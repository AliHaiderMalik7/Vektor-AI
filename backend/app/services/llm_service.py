from openai import OpenAI
import os
import json
import logging
import traceback
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any
from app.utils.helpers import stream_llm_response
from app.utils.system_message_fitness import FITNESS_SYSTEM_MESSAGE
from app.utils.unit_normalisation_and_bmi import normalize_and_bmi
from app.utils.json_utils import clean_json_response, try_parse_json

logger = logging.getLogger(__name__)
load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def generate_chatgpt_response(
        self,
        prompt: str,
        model: str = "gpt-4o",
        history: Optional[List[Dict[str, str]]] = None,
        system_message: str = FITNESS_SYSTEM_MESSAGE,
        max_tokens: int = 1500,
        temperature: float = 0.7,
        enable_web_search: bool = False,
        weight_value: Optional[float] = None,
        weight_unit: Optional[str] = None,
        height_value: Optional[float] = None,
        height_unit: Optional[str] = None,
        height_extra_inches: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Generate a structured response using OpenAI GPT models, with optional BMI context
        and auto-parsing of JSON-formatted responses.
        """
        try:
            logger.info(f"Generating response (model={model}, web_search={enable_web_search})")

            # Build message history
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

            # Append BMI details into the prompt for better fitness plan relevance
            if bmi_context:
                prompt = (
                    f"{prompt}\n\nSystem-provided metrics:\n"
                    f"- Normalized Weight: {bmi_context.get('normalized_weight_kg')} kg\n"
                    f"- Normalized Height: {bmi_context.get('normalized_height_cm')} cm\n"
                    f"- BMI: {bmi_context.get('bmi')}\n"
                    f"- BMI Category: {bmi_context.get('bmi_category')}"
                )

            messages.append({"role": "user", "content": prompt})

            # Call OpenAI Responses API
            response = self.client.responses.create(
                model=model,
                input=messages,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            # Try direct structured output first
            try:
                if hasattr(response, "output_parsed") and response.output_parsed:
                    parsed = response.output_parsed
                    if hasattr(parsed, "model_dump"):
                        return parsed.model_dump()
                    if isinstance(parsed, dict):
                        return parsed
                    if isinstance(parsed, str):
                        try:
                            return json.loads(parsed)
                        except json.JSONDecodeError:
                            return {"text": parsed}
                    return {"data": parsed}
            except Exception:
                logger.debug("output_parsed check failed, falling back to text extraction", exc_info=True)

            # Try output_text if available
            try:
                if hasattr(response, "output_text") and response.output_text:
                    parsed = try_parse_json(response.output_text)
                    if parsed is not None:
                        return parsed
                    return {"text": response.output_text}
            except Exception:
                logger.debug("response.output_text check failed; continuing", exc_info=True)

            # Fallback: iterate through response.output
            try:
                if hasattr(response, "output") and response.output:
                    for block in response.output:
                        content_list = None
                        if isinstance(block, dict):
                            content_list = block.get("content") or []
                        else:
                            content_list = getattr(block, "content", []) or []

                        for piece in content_list:
                            piece_type = None
                            piece_text = None

                            if isinstance(piece, dict):
                                piece_type = piece.get("type")
                                piece_text = piece.get("text") or piece.get("content") or None
                                if piece_text is None and isinstance(piece.get("content"), str):
                                    piece_text = piece.get("content")
                            else:
                                piece_type = getattr(piece, "type", None)
                                piece_text = getattr(piece, "text", None) or getattr(piece, "value", None)

                            if piece_type in ("output_text", "output_text_delta", "message"):
                                if hasattr(piece_text, "value"):
                                    piece_text = piece_text.value
                                if isinstance(piece_text, str):
                                    parsed = try_parse_json(piece_text)
                                    if parsed is not None:
                                        return parsed
                                    return {"text": piece_text}

                        maybe_text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
                        if hasattr(maybe_text, "value"):
                            maybe_text = maybe_text.value

                        if isinstance(maybe_text, str) and maybe_text.strip():
                            parsed = try_parse_json(maybe_text)
                            if parsed is not None:
                                return parsed
                            return {"text": maybe_text}

            except Exception:
                logger.debug("Iterating response.output failed", exc_info=True)

            # If no valid output was parsed
            logger.error("No valid response content could be extracted from OpenAI response.")
            return {"error": "No valid response content."}

        except Exception as e:
            logger.error(f"LLM service error: {e}")
            logger.error(traceback.format_exc())
            return {"error": f"LLM service error: {str(e)}"}