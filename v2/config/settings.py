"""
==========================================================
Application Settings

Purpose
-------
Central configuration for ProductChangeAnalyzer V2.

Responsibilities
----------------
✓ OpenAI configuration
✓ File paths
✓ PDF processing settings
✓ Logging configuration
✓ Report configuration

Business constants belong in constants.py

==========================================================
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Load environment variables from v2/.env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLES_FOLDER = PROJECT_ROOT / "samples"

OUTPUT_FOLDER = PROJECT_ROOT / "output"

PROMPTS_FOLDER = PROJECT_ROOT / "prompts"


# ==========================================================
# OpenAI Configuration
# ==========================================================

# Read the API key from an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model to use
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini"
)

# Model Parameters
TEMPERATURE = 0.0
MAX_TOKENS = 4000


# ==========================================================
# PDF Processing
# ==========================================================

MAX_PDF_SIZE_MB = 50

MAX_PAGES_PER_CHUNK = 20

EXTRACT_IMAGES = False


# ==========================================================
# JSON Extraction
# ==========================================================

JSON_RETRY_COUNT = 3

VALIDATE_JSON_RESPONSE = True


# ==========================================================
# Report Generation
# ==========================================================

GENERATE_EXCEL = True

GENERATE_WORD = False

GENERATE_JSON = True


# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

LOG_TO_FILE = True

LOG_FILE_NAME = "product_change_analyzer.log"


# ==========================================================
# Application
# ==========================================================

APPLICATION_NAME = "ProductChangeAnalyzer"

APPLICATION_VERSION = "2.0.0"

AUTHOR = "Prashil Wanjari"


# ==========================================================
# Ensure Required Folders Exist
# ==========================================================

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

DB_HOST = os.getenv("DB_HOST", "localhost")

DB_PORT = os.getenv("DB_PORT", "5432")

DB_NAME = os.getenv("DB_NAME", "product_change_analyzer")

DB_USER = os.getenv("DB_USER", "postgres")

DB_PASSWORD = os.getenv("DB_PASSWORD", "")