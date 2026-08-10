import yfinance as yf


# ============================================================
# GHANIYAA MARKET UNIVERSE
# ============================================================
#
# IMPORTANT:
# This is currently the bootstrap/discovery list.
#
# Later, this function can be connected to a complete NSE
# security-master source without changing the rest of Ghaniyaa.
#
# NSE symbol and Yahoo Finance symbol are deliberately kept
# separate.
#
# Example:
#
# NSE symbol:
#     TCS
#
# Yahoo symbol:
#     TCS.NS
#
# ============================================================

NSE_SYMBOLS = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "LT",
    "ITC",
    "BHARTIARTL",
    "HINDUNILVR",
    "HCLTECH",
    "WIPRO",
    "KOTAKBANK",
    "ONGC",
    "SUNPHARMA",
    "CIPLA",
    "MARUTI",
    "TATAMOTORS",
]


# ============================================================
# SYMBOL ALIASES
# ============================================================
#
# Some securities can change symbols over time.
#
# Keep aliases here rather than modifying the rest of the
# application.
#
# This also gives us a place to handle future symbol changes.
# ============================================================

SYMBOL_ALIASES = {
    # Example structure:
    #
    # "OLD_SYMBOL": "NEW_SYMBOL",
}


# ============================================================
# NORMALIZE SYMBOL
# ============================================================

def normalize_symbol(symbol: str) -> str:

    if not symbol:
        return ""

    symbol = (
        str(symbol)
        .strip()
        .upper()
    )

    # Remove Yahoo Finance suffix if supplied.
    if symbol.endswith(".NS"):
        symbol = symbol[:-3]

    # Apply known symbol alias.
    symbol = SYMBOL_ALIASES.get(
        symbol,
        symbol
    )

    return symbol


# ============================================================
# GET YAHOO SYMBOL
# ============================================================

def get_yahoo_symbol(symbol: str) -> str:

    symbol = normalize_symbol(symbol)

    if not symbol:
        return ""

    return symbol + ".NS"


# ============================================================
# GET NSE EQUITY UNIVERSE
# ============================================================
#
# This function provides the raw NSE universe.
#
# It deliberately does NOT call Yahoo Finance.
#
# That is important because:
#
# NSE universe discovery
#        !=
# Yahoo Finance validation
#
# Later we can replace only this function with a complete
# exchange/security-master discovery mechanism.
# ============================================================

def get_nse_equity_universe():

    results = []

    seen = set()

    for raw_symbol in NSE_SYMBOLS:

        symbol = normalize_symbol(
            raw_symbol
        )

        if not symbol:
            continue

        if symbol in seen:
            continue

        seen.add(symbol)

        results.append({
            "symbol": symbol,
            "yahoo_symbol": get_yahoo_symbol(symbol)
        })

    return results


# ============================================================
# VALIDATE ONE STOCK
# ============================================================

def validate_market_symbol(symbol: str):

    symbol = normalize_symbol(symbol)

    if not symbol:

        return {
            "symbol": "",
            "valid": False,
            "reason": "Empty symbol"
        }

    yahoo_symbol = get_yahoo_symbol(
        symbol
    )

    try:

        ticker = yf.Ticker(
            yahoo_symbol
        )

        info = ticker.info

        # ----------------------------------------------------
        # Determine whether Yahoo actually returned a security
        # ----------------------------------------------------

        company = info.get(
            "longName"
        )

        if not company:

            return {
                "symbol": symbol,
                "yahoo_symbol": yahoo_symbol,
                "valid": False,
                "reason": "Yahoo Finance returned no company information"
            }

        # ----------------------------------------------------
        # Extract metadata
        # ----------------------------------------------------

        sector = info.get(
            "sector",
            "Unknown"
        )

        exchange = info.get(
            "exchange",
            "NSI"
        )

        quote_type = info.get(
            "quoteType",
            "EQUITY"
        )

        # ----------------------------------------------------
        # Basic equity validation
        # ----------------------------------------------------

        if quote_type not in (
            "EQUITY",
            "STOCK"
        ):

            return {
                "symbol": symbol,
                "yahoo_symbol": yahoo_symbol,
                "valid": False,
                "reason": (
                    f"Yahoo quote type is {quote_type}"
                )
            }

        return {

            "symbol": symbol,

            "yahoo_symbol": yahoo_symbol,

            "valid": True,

            "company": company,

            "sector": sector,

            "exchange": exchange,

            "quote_type": quote_type
        }

    except Exception as e:

        return {

            "symbol": symbol,

            "yahoo_symbol": yahoo_symbol,

            "valid": False,

            "reason": str(e)
        }


# ============================================================
# VALIDATE COMPLETE MARKET UNIVERSE
# ============================================================

def validate_market_universe():

    results = []

    universe = get_nse_equity_universe()

    for stock in universe:

        symbol = stock["symbol"]

        result = validate_market_symbol(
            symbol
        )

        results.append(result)

    return results


# ============================================================
# GET MARKET UNIVERSE
# ============================================================
#
# Returns only VALID stocks.
#
# This is what universe_sync.py should use when adding stocks
# to Ghaniyaa's active registry.
# ============================================================

def get_market_universe():

    validation_results = (
        validate_market_universe()
    )

    valid_stocks = []

    for stock in validation_results:

        if not stock.get("valid"):
            continue

        valid_stocks.append({

            "symbol": stock["symbol"],

            "company": stock.get(
                "company",
                stock["symbol"]
            ),

            "sector": stock.get(
                "sector",
                "Unknown"
            ),

            "exchange": stock.get(
                "exchange",
                "NSI"
            ),

            "yahoo_symbol": stock.get(
                "yahoo_symbol"
            )
        })

    return valid_stocks


# ============================================================
# GET MARKET SYMBOLS
# ============================================================

def get_market_symbols():

    return [
        stock["symbol"]
        for stock in get_market_universe()
    ]


# ============================================================
# GET COMPLETE VALIDATION REPORT
# ============================================================
#
# Unlike get_market_universe(), this function includes both
# valid and invalid stocks.
#
# Useful for diagnostics and the /universe/test endpoint.
# ============================================================

def get_market_validation_report():

    results = validate_market_universe()

    valid = [
        stock
        for stock in results
        if stock.get("valid") is True
    ]

    invalid = [
        stock
        for stock in results
        if stock.get("valid") is False
    ]

    return {

        "total": len(results),

        "valid": len(valid),

        "invalid": len(invalid),

        "stocks": results
    }