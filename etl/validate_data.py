from utils import load_json, save_json, RAW_FILE, CLEAN_FILE
import logging

REQUIRED_FIELDS = ["symbol", "price", "volume"]

def validate_quotes():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"{RAW_FILE} not found. Run fetch_data.py first.")

    raw = load_json(RAW_FILE)
    valid = []
    bad = []

    for item in raw:
        missing = [f for f in REQUIRED_FIELDS if f not in item or item[f] is None]
        if missing:
            bad.append({"item": item, "missing": missing})
            continue

        # example: ignore negative prices/volumes
        if item["price"] <= 0 or item["volume"] < 0:
            bad.append({"item": item, "reason": "negative price/volume"})
            continue

        valid.append(item)

    save_json(CLEAN_FILE, valid)
    logging.info(f"Valid: {len(valid)} | Bad: {len(bad)}")
    if bad:
        logging.info("Some records were dropped during validation.")

if __name__ == "__main__":
    validate_quotes()
