import yfinance as yf


def get_stock(symbol):
    ticker = yf.Ticker(f"{symbol}.NS")

    info = ticker.info

    hist = ticker.history(period="1mo")

    return {
        "symbol": symbol,
        "company": info.get("longName", symbol),
        "price": info.get("currentPrice", 0),
        "pe": info.get("trailingPE", "N/A"),
        "roe": info.get("returnOnEquity", "N/A"),
        "history": {
            "dates": [str(d.date()) for d in hist.index],
            "prices": [round(float(x), 2) for x in hist["Close"]],
        },
    }


def compare(symbol1, symbol2):
    return {
        "stock1": get_stock(symbol1),
        "stock2": get_stock(symbol2),
    }