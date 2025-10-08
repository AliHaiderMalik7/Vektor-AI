import logging
from typing import Generator, Any
import json

logger = logging.getLogger(__name__)

# helpers.py
def stream_llm_response(response_stream: Any) -> Generator[str, None, None]:
    """Stream LLM response chunks as plain text."""
    try:
        for chunk in response_stream:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    yield delta.content  # Just yield the text
    except Exception as e:
        logger.error(f"Error streaming response: {str(e)}")
        raise