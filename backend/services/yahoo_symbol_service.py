# backend/services/yahoo_symbol_service.py

from backend.stock_registry import get_stock_info


def get_yahoo_symbol(symbol: str) -> str:
    """
    Return correct Yahoo symbol.

    Priority:
    1. NSE
    2. BSE
    3. Fallback NSE
    """

    if not symbol:
        return ""

    symbol = str(symbol).strip().upper()

    stock = get_stock_info(symbol)

    if stock:

        nse = stock.get("nse_yahoo_symbol")
        if nse:
            return nse

        bse = stock.get("bse_yahoo_symbol")
        if bse:
            return bse

    return f"{symbol}.NS"