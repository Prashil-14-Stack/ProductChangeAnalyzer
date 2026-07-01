# ==========================================
# OpenAI Configuration
# ==========================================
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_MODEL = "gpt-4o-mini"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_PROVIDER = "OPENAI"

LLM_TIMEOUT = 30

LLM_PROVIDER = "ENTERPRISE"