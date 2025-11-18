from fastapi import APIRouter
from db.connection import get_connection

router = APIRouter()

@router.get("/top-gainers")
def top_gainers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT symbol, price, change, change_percent 
        FROM stock_quotes
        ORDER BY change DESC
        LIMIT 5;
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {"symbol": r[0], "price": r[1], "change": r[2], "change_percent": r[3]}
        for r in rows
    ]

@router.get("/avg-volume/{symbol}")
def avg_volume(symbol: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT AVG(volume)
        FROM stock_quotes
        WHERE symbol = %s;
    """, (symbol.upper(),))

    avg_volume = cur.fetchone()[0]
    conn.close()

    return {"symbol": symbol.upper(), "avg_volume": avg_volume}
