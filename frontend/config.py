import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL")

# Secret Key for JWT authentication
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithm for JWT authentication
ALGORITHM = os.getenv("ALGORITHM")

# Expiration time for JWT authentication
EXPIRATION_MINUTES = os.getenv("EXPIRATION_MINUTES")

# Postgres
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
