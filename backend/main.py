from fastapi import FastAPI

app = FastAPI(
    title="Ghaniyaa Stocks API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Ghaniyaa Stocks API 🚀"
    }


@app.get("/stock/{symbol}")
def analyze_stock(symbol: str):
    sample_data = {
        "TCS": {
            "company": "Tata Consultancy Services",
            "score": 92,
            "rating": "Excellent"
        },
        "RELIANCE": {
            "company": "Reliance Industries",
            "score": 90,
            "rating": "Very Good"
        },
        "INFY": {
            "company": "Infosys",
            "score": 88,
            "rating": "Very Good"
        }
    }

    stock = sample_data.get(symbol.upper())

    if stock:
        return {
            "symbol": symbol.upper(),
            "company": stock["company"],
            "ghaniyaa_score": stock["score"],
            "rating": stock["rating"],
            "ai_summary": "This is a sample AI analysis. Live market data will be added later."
        }

    return {
        "error": "Stock not found"
    }