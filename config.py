import os
from dotenv import load_dotenv

# Build path to .env file in project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')

# Load environment variables
load_dotenv(dotenv_path)

# Read API key & city list
API_KEY = os.getenv("API_KEY")
CITY_LIST = os.getenv("CITIES", "Memphis").split(",")

# PostgreSQL Database configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "weatherdb"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Hyderabad@24"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432))
}

# SQLite (optional fallback)
DB_PATH = "data/weather.db"
