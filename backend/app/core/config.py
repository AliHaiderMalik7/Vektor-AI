import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # Default Models
    DEFAULT_OPENAI_MODEL: str = "gpt-4o-mini"

    # CORS Configuration
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8000",  # frontend local dev
        "http://127.0.0.1:8000",
        # "https://yourfrontenddomain.com"  # production
    ]

    class Config:
        env_file = ".env"

settings = Settings()
