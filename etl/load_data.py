from etl.utils import load_json, CLEAN_FILE
from db.connection import get_connection
import logging

def ensure_table(conn):
    create_sql = """
    CREATE TABLE IF NOT EXISTS stock_quotes (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL,
        price NUMERIC(12,4),
        volume BIGINT,
        market_cap NUMERIC(20,2),
        fetched_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_sql)
    conn.commit()

def load_quotes():
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"{CLEAN_FILE} not found. Run validate_data.py first.")

    data = load_json(CLEAN_FILE)
    if not data:
        logging.info("No data to load. Clean file is empty.")
        return

    conn = get_connection()
    ensure_table(conn)

    insert_sql = """
    INSERT INTO stock_quotes (symbol, price, volume, market_cap)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """

    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                insert_sql,
                (
                    item.get("symbol"),
                    item.get("price"),
                    item.get("volume"),
                    item.get("marketCap"),
                ),
            )
    conn.commit()
    conn.close()
    logging.info(f"Loaded {len(data)} rows into stock_quotes")

if __name__ == "__main__":
    load_quotes()
