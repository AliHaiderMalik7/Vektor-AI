from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

chat_completion = client.chat.completions.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="Did Pakistan win 2025 Asia Cup?"
)

print(chat_completion.output_text)