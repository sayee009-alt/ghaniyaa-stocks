import yfinance as yf

from backend.stock_registry import get_all_symbols
from backend.services.market_universe import (
    get_nse_equity_universe
)


def validate_stock(symbol: str):

    symbol = symbol.strip().upper()

    if not symbol:
        return {
            "symbol": symbol,
            "valid": False
        }

    try:

        ticker = yf.Ticker(
            get_yahoo_symbol(symbol)
        )

        info = ticker.info

        company = info.get(
            "longName"
        )

        if company:

            return {
                "symbol": symbol,
                "valid": True,
                "company": company,
                "sector": info.get(
                    "sector",
                    "Unknown"
                ),
                "exchange": info.get(
                    "exchange",
                    "NSE"
                )
            }

    except Exception as e:

        print(
            f"Universe validation error for {symbol}: {e}"
        )

    return {
        "symbol": symbol,
        "valid": False
    }


def validate_current_universe():

    symbols = get_all_symbols()

    results = []

    for symbol in symbols:

        result = validate_stock(symbol)

        results.append(result)

    return results


def get_valid_symbols():

    results = validate_current_universe()

    return [
        item["symbol"]
        for item in results
        if item["valid"]
    ]
def discover_nse_stocks():

    stocks = get_nse_equity_universe()

    return stocks