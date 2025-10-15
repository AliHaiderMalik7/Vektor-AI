import logging
import re
import json

logger = logging.getLogger(__name__)

def stream_llm_response(response_stream):
    """Stream OpenAI responses as SSE with HTML-safe spacing and list formatting."""
    try:
        buffer = ""
        for event in response_stream:
            if event.type == "response.output_text.delta":
                chunk = event.delta
                buffer += chunk

                # Normalize spaces
                buffer = re.sub(r'\s+', ' ', buffer)

                # Convert markdown-like formatting into HTML
                buffer = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', buffer)  # bold
                buffer = re.sub(r'__([^_]+)__', r'<b>\1</b>', buffer)    # alternative bold

                # Add <br> before bullets and numbered lists
                buffer = re.sub(r'\s*([•\-–*]\s+)', r'<br>\1', buffer)
                buffer = re.sub(r'\s*(\d+\.\s+)', r'<br>\1', buffer)

                # Add <br> before section markers
                buffer = re.sub(r'\s*(#{1,6}\s+)', r'<br>\1', buffer)

                # Send whenever we have punctuation, space, or newline
                if any(x in chunk for x in [" ", "\n"]) or chunk.endswith((".", ",", "!", "?", ":")):
                    yield f"data: {buffer.strip()}\n\n"
                    buffer = ""

            elif event.type == "response.error":
                yield f"data: [ERROR] {event.error}\n\n"

        # Flush remaining text
        if buffer.strip():
            yield f"data: {buffer.strip()}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
