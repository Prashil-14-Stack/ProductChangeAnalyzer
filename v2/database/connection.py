"""
==========================================================
PostgreSQL Database Connection

Purpose
-------
Provides a centralized PostgreSQL database connection
for the Product Change Analyzer.

Database configuration is loaded from the project's
.env file.

==========================================================
"""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# ==========================================================
# Load .env
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ==========================================================
# Database Configuration
# ==========================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")


# ==========================================================
# Validate Configuration
# ==========================================================

missing_variables = []

if not DB_HOST:
    missing_variables.append("DB_HOST")

if not DB_NAME:
    missing_variables.append("DB_NAME")

if not DB_USER:
    missing_variables.append("DB_USER")

if not DB_PASSWORD:
    missing_variables.append("DB_PASSWORD")


if missing_variables:

    raise RuntimeError(
        "Missing database configuration: "
        + ", ".join(missing_variables)
        + f"\nExpected .env file: {ENV_FILE}"
    )


# ==========================================================
# Create Database Connection
# ==========================================================

def get_connection():

    connection = psycopg2.connect(

        host=DB_HOST,

        port=DB_PORT,

        database=DB_NAME,

        user=DB_USER,

        password=DB_PASSWORD

    )

    return connection


# ==========================================================
# Test Database Connection
# ==========================================================

def test_connection():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT version();")

        version = cursor.fetchone()[0]

        cursor.close()

        print("========================================")
        print("PostgreSQL connection successful!")
        print("========================================")
        print(f"Database: {DB_NAME}")
        print(f"Host: {DB_HOST}")
        print(f"Port: {DB_PORT}")
        print(f"Schema: {DB_SCHEMA}")
        print("----------------------------------------")
        print("PostgreSQL version:")
        print(version)
        print("========================================")

        return True

    except Exception as error:

        print("========================================")
        print("PostgreSQL connection FAILED")
        print("========================================")
        print(error)

        return False

    finally:

        if connection:

            connection.close()