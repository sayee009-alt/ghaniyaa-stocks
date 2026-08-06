import yfinance as yf
from backend.services.score import calculate_score

NSE_STOCKS = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "LT",
    "ITC",
    "HCLTECH",
    "TECHM"
]



def screen_all_stocks():
    results = []

    for symbol in NSE_STOCKS:
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.info

            results.append({
                "symbol": symbol,
                "company": info.get("longName"),
                "price": info.get("currentPrice"),
                "sector": info.get("sector"),
                "marketCap": info.get("marketCap"),
                "pe": info.get("trailingPE"),
                "roe": info.get("returnOnEquity"),
                "score": calculate_score(info)
            })

        except Exception:
            pass

    return results