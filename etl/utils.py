from pathlib import Path
import json
import time
import logging
import yaml

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_FILE = DATA_DIR / "raw_quotes.json"
CLEAN_FILE = DATA_DIR / "clean_quotes.json"

# Make sure data/ exists
DATA_DIR.mkdir(exist_ok=True)

# Simple logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def load_config():
    """Load YAML config from etl/config.yaml"""
    cfg_path = BASE_DIR / "config.yaml"
    with open(cfg_path, "r") as f:
        return yaml.safe_load(f)

def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def retry_request(func, retries=3, delay=2):
    """Tiny retry helper for API calls."""
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise
            time.sleep(delay)
