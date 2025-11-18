from fastapi import FastAPI
from api.routers import stocks, analytics

app = FastAPI(
    title="FinDataFlow API",
    description="Enterprise Data Delivery API (Stocks, Analytics, ETL Data)",
    version="1.0.0"
)

# Include Routers
app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}
