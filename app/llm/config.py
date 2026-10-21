import os

from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "openai/gpt-oss-20b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
