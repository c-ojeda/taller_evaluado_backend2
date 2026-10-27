import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Carga el .env ubicado en la raíz del proyecto.
project_root = Path(__file__).resolve().parents[2]
load_dotenv(project_root / ".env")


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", os.getenv("POSTGRES_PORT", "5432"))),
        dbname=os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "taller_db")),
        user=os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres")),
        password=os.getenv(
            "DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "")
        ),
    )