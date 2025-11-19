# etl/fetch_data.py
import requests
import logging
from etl.utils import load_config, save_json, RAW_FILE

def fetch_quotes():
    cfg = load_config()
    api_cfg = cfg["api"]
    symbols = cfg["etl"]["symbols"]

    base_url = api_cfg["base_url"]
    api_key = api_cfg["key"]       

    all_quotes = []

    for sym in symbols:
        url = f"{base_url}?function=GLOBAL_QUOTE&symbol={sym}&apikey={api_key}"
        logging.info(f"Fetching {sym} from AlphaVantage")

        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            cleaned = {
                "symbol": quote.get("01. symbol"),
                "price": float(quote.get("05. price", 0)),
                "volume": int(quote.get("06. volume", 0)),
                "previous_close": float(quote.get("08. previous close", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent", "0%")
            }
            all_quotes.append(cleaned)
        else:
            logging.warning(f"No data returned for {sym}: {data}")

    save_json(RAW_FILE, all_quotes)
    logging.info(f"Saved {len(all_quotes)} quotes → {RAW_FILE}")

if __name__ == "__main__":
    fetch_quotes()
