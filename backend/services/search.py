import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STOCKS_FILE = BASE_DIR / "database" / "stocks.json"
print("Stocks file:", STOCKS_FILE)
print("Exists:", STOCKS_FILE.exists())

def search_stock(query: str):
    query = query.lower()

    with open(STOCKS_FILE, "r") as f:
        stocks = json.load(f)

    results = []

    for stock in stocks:
        if (
            query in stock["symbol"].lower()
            or query in stock["company"].lower()
        ):
            results.append(stock)

    return results