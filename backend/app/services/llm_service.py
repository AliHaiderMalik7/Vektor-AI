from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Generator
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
        system_message: str = "You are a helpful travel assistant. Ask clarifying questions if needed.",
        max_tokens: int = 500,
        temperature: float = 0.7,
        enable_web_search: bool = False,
        stream: bool = False,  # New parameter
    ):
        try:
            logger.info(f"Generating response with web_search={enable_web_search}, stream={stream}")
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]

            tools = [{"type": "web_search"}] if enable_web_search else None

            response = self.client.responses.create(
                model=model,
                input=messages,
                tools=tools,
                temperature=temperature,
                max_output_tokens=max_tokens,
                stream=stream,  # Enable streaming
            )

            # If streaming, return generator
            if stream:
                return stream_llm_response(response)
            
            # If not streaming, return complete response
            if hasattr(response, "output_text") and response.output_text:
                reply = response.output_text.strip()
                logger.info(f"Response: {reply[:200]}...")
                return reply
            else:
                return "No response generated."

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"LLM service error: {str(e)}")