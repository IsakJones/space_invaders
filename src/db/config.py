"""
DOCSTRING

Loads environment variables and generates database connection URI.
"""

from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os

load_dotenv()

URI = URL(
    "postgresql+psycopg2",
    os.getenv("DBUSER"),
    os.getenv("DBPASS"),
    os.getenv("DBHOST"),
    os.getenv("DBPORT"),
    os.getenv("DBNAME")
)
