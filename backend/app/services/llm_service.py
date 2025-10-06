from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# prompt = "Explain the theory of relativity in simple terms."
prompt = input("Enter your prompt: ")

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that provide clear and concise explanations."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    model = "gpt-4o",
    max_tokens=250,
    temperature=0.9,
    top_p=0.5
)

print(chat_completion.choices[0].message.content)