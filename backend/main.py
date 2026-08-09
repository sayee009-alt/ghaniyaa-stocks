from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
from backend.routes.watchlist import load_watchlist, save_watchlist
from backend.routes.screener import router as screener_router
from backend.routes.search import router as search_router
from backend.routes.portfolio import router as portfolio_router
from backend.routes.advisor import router as advisor_router
from backend.routes.prediction import router as prediction_router
from backend.routes.decision import router as decision_router
from backend.routes.thesis import router as thesis_router

app = FastAPI()

app.include_router(screener_router)
app.include_router(search_router)
app.include_router(portfolio_router)
app.include_router(advisor_router)
app.include_router(prediction_router)
app.include_router(decision_router)
app.include_router(thesis_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stocks = {
    "TCS": {
        "company": "Tata Consultancy Services",
        "score": 92,
        "rating": "Excellent"
    },
    "INFY": {
        "company": "Infosys",
        "score": 89,
        "rating": "Very Good"
    },
    "RELIANCE": {
        "company": "Reliance Industries",
        "score": 90,
        "rating": "Excellent"
    }
}

@app.get("/")
def home():
    return {"message": "Ghaniyaa Stocks API Running"}

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    symbol = symbol.upper()

    if symbol in stocks:
        return stocks[symbol]

    return {
        "company": "Unknown",
        "score": 0,
        "rating": "Not Found"
    }


@app.get("/live/{symbol}")
def live_stock(symbol: str):

    stock = yf.Ticker(symbol + ".NS")
    info = stock.info

    return {
        "company": info.get("longName", "Unknown"),
        "price": info.get("currentPrice", "N/A"),
        "marketCap": info.get("marketCap", "N/A"),
        "sector": info.get("sector", "Unknown")
    }
@app.get("/score/{symbol}")
def ghaniyaa_score(symbol: str):

    stock = yf.Ticker(symbol + ".NS")
    info = stock.info

    score = 50

    pe = info.get("trailingPE")

    if pe and pe < 25:
        score += 15

    roe = info.get("returnOnEquity")

    if roe and roe > 0.15:
        score += 20

    debt = info.get("debtToEquity")

    if debt and debt < 50:
        score += 15

    if score > 100:
        score = 100

    return {
        "company": info.get("longName"),
        "ghaniyaa_score": score
    }
@app.get("/history/{symbol}")
def stock_history(symbol: str):

    stock = yf.Ticker(symbol + ".NS")

    history = stock.history(period="1mo")

    dates = history.index.strftime("%Y-%m-%d").tolist()
    prices = history["Close"].round(2).tolist()

    return {
        "dates": dates,
        "prices": prices
    }
@app.get("/financials/{symbol}")
def financials(symbol: str):

    stock = yf.Ticker(symbol + ".NS")
    info = stock.info

    return {
        "pe_ratio": info.get("trailingPE", "N/A"),
        "roe": info.get("returnOnEquity", "N/A"),
        "debt_to_equity": info.get("debtToEquity", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "market_cap": info.get("marketCap", "N/A")
    }
@app.get("/summary/{symbol}")
def summary(symbol: str):

    stock = yf.Ticker(symbol + ".NS")
    info = stock.info

    company = info.get("longName", symbol)

    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity")
    debt = info.get("debtToEquity")

    summary = f"{company}: "

    if roe and roe > 0.15:
        summary += "The company has strong profitability. "
    else:
        summary += "Profitability appears average. "

    if debt and debt < 50:
        summary += "Debt levels are healthy. "
    else:
        summary += "Debt levels should be reviewed carefully. "

    if pe and pe < 25:
        summary += "Valuation looks reasonable. "
    else:
        summary += "The stock may be trading at a premium valuation. "

    summary += "This is an automated summary for educational purposes and should not be considered investment advice."

    return {
        "company": company,
        "summary": summary
    }
@app.post("/watchlist/{symbol}")
def add_to_watchlist(symbol: str):

    watchlist = load_watchlist()

    symbol = symbol.upper()

    if symbol not in watchlist:
        watchlist.append(symbol)
        save_watchlist(watchlist)

    return {
        "watchlist": watchlist
    }
@app.get("/watchlist")
def get_watchlist():
    return {
        "watchlist": load_watchlist()
    }
@app.get("/compare/{symbol1}/{symbol2}")
def compare(symbol1: str, symbol2: str):

    stock1 = yf.Ticker(symbol1.upper() + ".NS")
    stock2 = yf.Ticker(symbol2.upper() + ".NS")

    info1 = stock1.info
    info2 = stock2.info

    history1 = stock1.history(period="1mo")
    history2 = stock2.history(period="1mo")

    pe1 = info1.get("trailingPE") or 999
    pe2 = info2.get("trailingPE") or 999

    roe1 = info1.get("returnOnEquity") or 0
    roe2 = info2.get("returnOnEquity") or 0

    score1 = 0
    score2 = 0

    # Higher price
    if info1.get("currentPrice", 0) > info2.get("currentPrice", 0):
        score1 += 1
    else:
        score2 += 1

    # Lower PE
    if pe1 < pe2:
        score1 += 1
    else:
        score2 += 1

    # Higher ROE
    if roe1 > roe2:
        score1 += 1
    else:
        score2 += 1

    print("Score1 =", score1)
    print("Score2 =", score2)

    if score1 > score2:
        winner = symbol1.upper()
        reason = "Better valuation and profitability."
    elif score2 > score1:
        winner = symbol2.upper()
        reason = "Better valuation and profitability."
    else:
        winner = "Tie"
        reason = "Both stocks have similar fundamentals."

    return {
        "stock1": {
            "symbol": symbol1.upper(),
            "company": info1.get("longName"),
            "price": info1.get("currentPrice"),
            "pe": pe1,
            "roe": roe1,
            "history": {
                "dates": history1.index.strftime("%Y-%m-%d").tolist(),
                "prices": history1["Close"].round(2).tolist()
            }
        },
        "stock2": {
            "symbol": symbol2.upper(),
            "company": info2.get("longName"),
            "price": info2.get("currentPrice"),
            "pe": pe2,
            "roe": roe2,
            "history": {
                "dates": history2.index.strftime("%Y-%m-%d").tolist(),
                "prices": history2["Close"].round(2).tolist()
            }
        },
        "winner": winner,
        "reason": reason
    }
@app.get("/news/{symbol}")
def stock_news(symbol: str):
    return {
        "news": [
            {
                "title": f"{symbol.upper()} announces quarterly results",
                "source": "Ghaniyaa Demo",
                "url": "#"
            },
            {
                "title": f"{symbol.upper()} expands AI business",
                "source": "Ghaniyaa Demo",
                "url": "#"
            },
            {
                "title": f"Analysts discuss {symbol.upper()} outlook",
                "source": "Ghaniyaa Demo",
                "url": "#"
            }
        ]
    }

