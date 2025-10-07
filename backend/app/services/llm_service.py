from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

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
    ) -> str:
        try:
            # ✅ Automatically enable web search if query mentions flight or fare
            if any(word in prompt.lower() for word in ["flight", "fare", "ticket", "airline"]):
                enable_web_search = True

            logger.info(f"Generating response with web_search={enable_web_search}")

            # Prompt for the assistant
            clarification_prompt = f"""
You are a professional travel planner.

If the user's message lacks key details (dates, travelers, budget, or hotel type), ask follow-up questions.

If all details are provided:
1. Create a full 5-day itinerary (morning, afternoon, evening).
2. Recommend 3 hotels with nightly cost in GBP.
3. Give the **total estimated cost in GBP**.
4. Use **web search** (if available) to find **real flight fare ranges** from Lahore to London (lowest ↔ highest) for the given dates.
5. Include 2–3 must-visit tourist sites per day.

User prompt:
{prompt}
            """

            # Enable OpenAI’s web search tool
            tools = [{"type": "web_search"}] if enable_web_search else None

            # Send to OpenAI
            response = self.client.responses.create(
                model=model,
                input=clarification_prompt,
                tools=tools,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            # Extract output
            if hasattr(response, "output_text") and response.output_text:
                reply = response.output_text.strip()
                logger.info(f"Response: {reply[:200]}...")
                return reply
            else:
                return "No response generated."

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"LLM service error: {str(e)}")