from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Stock(BaseModel):
    symbol: str
    price: float
    volume: int
    market_cap: Optional[float] = None
    fetched_at: str

@router.get("/", response_model=List[Stock])
def get_all_stocks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT symbol, price, volume, market_cap, fetched_at
        FROM stock_quotes
        ORDER BY fetched_at DESC
        LIMIT 50;
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No stock data found")

    return [
        Stock(
            symbol=row[0],
            price=row[1],
            volume=row[2],
            market_cap=row[3],
            fetched_at=row[4].isoformat(),
        )
        for row in rows
    ]

@router.get("/{symbol}", response_model=Stock)
def get_stock_by_symbol(symbol: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT symbol, price, volume, market_cap, fetched_at
        FROM stock_quotes
        WHERE symbol = %s
        ORDER BY fetched_at DESC
        LIMIT 1;
    """, (symbol.upper(),))

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Symbol not found")

    return Stock(
        symbol=row[0],
        price=row[1],
        volume=row[2],
        market_cap=row[3],
        fetched_at=row[4].isoformat()
    )
