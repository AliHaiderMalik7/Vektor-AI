from openai import OpenAI
import os, json, logging, re, traceback
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any
from app.utils.helpers import stream_llm_response
from app.utils.system_message_fitness import FITNESS_SYSTEM_MESSAGE
from app.utils.unit_normalisation_and_bmi import normalize_and_bmi

logger = logging.getLogger(__name__)
load_dotenv()


class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    # small helper to clean JSON-like text returned by the model
    def _clean_json_response(self, response_text: str) -> str:
        if response_text is None:
            return ""
        logger.debug(f"Raw response_text for cleaning: {response_text!r}")

        # remove triple-backtick fences and any leading/trailing text outside the first {...} object
        cleaned = re.sub(r"```(?:json)?\s*", "", response_text)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        # try to extract first JSON object or array
        m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
        if m:
            cleaned = m.group(1)
        return cleaned.strip()

    def _try_parse_json(self, text: str) -> Optional[Any]:
        if text is None:
            return None
        text = re.sub(r"```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text).strip()

        # Match all JSON objects
        matches = re.findall(r'(\{[\s\S]*?\})(?=\{|\Z)', text)
        parsed_list = []
        for m in matches:
            try:
                parsed_list.append(json.loads(m))
            except json.JSONDecodeError:
                continue
        if not parsed_list:
            return None
        if len(parsed_list) == 1:
            return parsed_list[0]
        return parsed_list  # Return all JSON objects as a list


    def generate_chatgpt_response(
        self,
        prompt: str,
        model: str = "gpt-4o",
        history: Optional[List[Dict[str, str]]] = None,
        system_message: str = FITNESS_SYSTEM_MESSAGE,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        enable_web_search: bool = False,
        weight_value: Optional[float] = None,
        weight_unit: Optional[str] = None,
        height_value: Optional[float] = None,
        height_unit: Optional[str] = None,
        height_extra_inches: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Uses client.responses.create(...) and returns a dict:
         - If the model produced JSON matching a schema, returns that dict
         - Otherwise returns {"text": "..."} or {"error": "..."}
        This function intentionally does NOT use response_format/response_format parameter.
        """
        try:
            logger.info(f"Generating response (model={model}, web_search={enable_web_search})")

            # Build messages
            messages: List[Dict[str, str]] = [{"role": "system", "content": system_message}]
            if history:
                messages.extend(history)

            # BMI context if provided
            bmi_context = {}
            if weight_value and height_value:
                try:
                    bmi_context = normalize_and_bmi(
                        weight_value, weight_unit or "kg",
                        height_value, height_unit or "cm",
                        height_extra_inches
                    )
                    logger.info(f"BMI context: {bmi_context}")
                except Exception as e:
                    logger.warning(f"BMI normalization failed: {e}")

            if bmi_context:
                prompt = (
                    f"{prompt}\n\nSystem-provided metrics:\n"
                    f"- Normalized Weight: {bmi_context.get('normalized_weight_kg')} kg\n"
                    f"- Normalized Height: {bmi_context.get('normalized_height_cm')} cm\n"
                    f"- BMI: {bmi_context.get('bmi')}\n"
                    f"- BMI Category: {bmi_context.get('bmi_category')}"
                )

            messages.append({"role": "user", "content": prompt})

            # === CALL THE RESPONSES API (no response_format here) ===
            response = self.client.responses.create(
                model=model,
                input=messages,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            # Prefer output_parsed if available (structured JSON from server) ===
            try:
                if hasattr(response, "output_parsed") and response.output_parsed:
                    parsed = response.output_parsed
                    # parsed may be a Pydantic model or a plain dict
                    if hasattr(parsed, "model_dump"):
                        return parsed.model_dump()
                    if isinstance(parsed, dict):
                        return parsed
                    # if it's a string, try to json.loads it
                    if isinstance(parsed, str):
                        try:
                            return json.loads(parsed)
                        except json.JSONDecodeError:
                            return {"text": parsed}
                    # fallback: return as-is under data key
                    return {"data": parsed}
            except Exception:
                # don't fail entirely here — fall back to text extraction
                logger.debug("output_parsed check failed, falling back to text extraction", exc_info=True)

            # Try response.output_text (some SDKs provide this property) ===
            try:
                if hasattr(response, "output_text") and response.output_text:
                    # output_text should already be a plain string
                    parsed = self._try_parse_json(response.output_text)
                    if parsed is not None:
                        return parsed
                    # return {"text": response.output_text}
            except Exception:
                logger.debug("response.output_text check failed; continuing", exc_info=True)

            # Fall back to iterating response.output content blocks ===
            try:
                if hasattr(response, "output") and response.output:
                    for block in response.output:
                        # block might be a dict or a Pydantic model
                        content_list = None
                        if isinstance(block, dict):
                            content_list = block.get("content") or []
                        else:
                            content_list = getattr(block, "content", []) or []

                        # iterate content pieces
                        for piece in content_list:
                            # piece might be dict or object
                            piece_type = None
                            piece_text = None

                            if isinstance(piece, dict):
                                piece_type = piece.get("type")
                                # text might be under "text"
                                piece_text = piece.get("text") or piece.get("content") or None
                                # some shapes use "content" as list; try to stringify
                                if piece_text is None and isinstance(piece.get("content"), str):
                                    piece_text = piece.get("content")
                            else:
                                # pydantic-like object
                                piece_type = getattr(piece, "type", None)
                                # text attribute may be 'text' or 'value'
                                piece_text = getattr(piece, "text", None)
                                if piece_text is None:
                                    piece_text = getattr(piece, "value", None)

                            # if this piece is textual output, try parse JSON
                            if piece_type in ("output_text", "output_text_delta", "message"):
                                # piece_text may be a Pydantic string object or actual string
                                if hasattr(piece_text, "value"):
                                    piece_text = piece_text.value
                                if isinstance(piece_text, str):
                                    parsed = self._try_parse_json(piece_text)
                                    if parsed is not None:
                                        return parsed
                                    return {"text": piece_text}

                        # Some SDK shapes place textual output in block.text
                        if isinstance(block, dict):
                            maybe_text = block.get("text") or block.get("content")
                        else:
                            maybe_text = getattr(block, "text", None) or getattr(block, "content", None)

                        # normalize Pydantic wrapper
                        if hasattr(maybe_text, "value"):
                            maybe_text = maybe_text.value

                        if isinstance(maybe_text, str) and maybe_text.strip():
                            parsed = self._try_parse_json(maybe_text)
                            if parsed is not None:
                                return parsed
                            return {"text": maybe_text}

            except Exception:
                logger.debug("Iterating response.output failed", exc_info=True)

            # If no extraction succeeded
            logger.error("No valid response content could be extracted from OpenAI response.")
            return {"error": "No valid response content."}

        except Exception as e:
            logger.error(f"LLM service error: {e}")
            logger.error(traceback.format_exc())
            return {"error": f"LLM service error: {str(e)}"}