import yfinance as yf

from backend.stock_registry import get_stock_info
from backend.services.score import calculate_score
from backend.services.yahoo_ticker import get_yahoo_ticker


def get_stock_analysis(symbol: str):
    symbol = symbol.strip().upper()

    registry_info = get_stock_info(symbol)

    if not registry_info:
        return {
            "success": False,
            "symbol": symbol,
            "error": "Stock not found in Ghaniyaa universe"
        }

    yahoo_symbol = get_yahoo_ticker(symbol)

    try:
        ticker = yf.Ticker(yahoo_symbol)

        info = ticker.info

        company = info.get(
            "longName",
            registry_info.get("company", "Unknown")
        )

        current_price = info.get("currentPrice")

        sector = info.get(
            "sector",
            registry_info.get("sector", "Unknown")
        )

        if current_price is None:
            return {
                "success": False,
                "symbol": symbol,
                "company": company,
                "error": "Current market price is unavailable"
            }

        return {
            "success": True,
            "symbol": symbol,
            "company": company,
            "price": current_price,
            "sector": sector,
            "marketCap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "roe": info.get("returnOnEquity"),
            "profitMargin": info.get("profitMargins"),
            "revenueGrowth": info.get("revenueGrowth"),
            "earningsGrowth": info.get("earningsGrowth"),
            "dividendYield": info.get("dividendYield"),
            "52WeekHigh": info.get("fiftyTwoWeekHigh"),
            "52WeekLow": info.get("fiftyTwoWeekLow"),
            "score": calculate_score(info)
        }

    except Exception as e:
        print(
            f"Stock analysis error for "
            f"{symbol}: {e}"
        )

        return {
            "success": False,
            "symbol": symbol,
            "error": "Unable to retrieve market data"
        }