import os

from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


print("========================================")
print("Environment Test")
print("========================================")

print("ENV FILE:", ENV_FILE)

print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))

print("DB_PASSWORD:",
      "SET" if os.getenv("DB_PASSWORD") else "NOT SET")

print("========================================")