from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Generator, List, Dict, Optional
from app.utils.helpers import stream_llm_response

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
        model: str = "gpt-4o-mini",
        history: Optional[List[Dict[str, str]]] = None,
        system_message: str = "You are a helpful flight assistant. Ask clarifying questions if needed.",
        max_tokens: int = 500,
        temperature: float = 0.7,
        enable_web_search: bool = False,
        stream: bool = False,
    ) -> Generator[str, None, None] | str:
    
        try:
            logger.info(f"Generating response with web_search={enable_web_search}, stream={stream}")

            # Combine history + current user prompt
            messages = [{"role": "system", "content": system_message}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": prompt})

            # Optional tools setup
            tools = [{"type": "web_search"}] if enable_web_search else None

            # Call OpenAI API
            response = self.client.responses.create(
                model=model,
                input=messages,
                tools=tools,
                temperature=temperature,
                max_output_tokens=max_tokens,
                stream=stream
            )

            # If streaming, yield chunks
            if stream:
                logger.info("Streaming response...")
                return stream_llm_response(response)

            # If not streaming, return full text
            if hasattr(response, "output_text") and response.output_text:
                reply = response.output_text.strip()
                logger.info(f"Response: {reply[:200]}...")
                return reply
            else:
                return "No response generated."

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"LLM service error: {str(e)}")
