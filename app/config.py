import os
from dotenv import load_dotenv

load_dotenv()

CACHE_THRESHOLD = float(os.getenv("CACHE_THRESHOLD", "0.90"))

DB_PATH = os.getenv(
    "DB_PATH",
    "data/requests.db"
)
