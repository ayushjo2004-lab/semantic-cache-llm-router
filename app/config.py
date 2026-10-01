import os
from dotenv import load_dotenv

load_dotenv()

CACHE_THRESHOLD = float(os.getenv("CACHE_THRESHOLD", "0.90"))

MAX_ROUTE_COST = float(os.getenv("MAX_ROUTE_COST", "0.0003"))

DB_PATH = os.getenv(
    "DB_PATH",
    "data/requests.db"
)
