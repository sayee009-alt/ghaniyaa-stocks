from backend.stock_universe import STOCK_UNIVERSE


# -----------------------------------------
# GHANIYAA STOCK REGISTRY
# -----------------------------------------

def normalize_symbol(symbol: str) -> str:
    """
    Convert a stock symbol into Ghaniyaa's
    standard format.
    """

    return symbol.strip().upper()


# -----------------------------------------
# Check whether stock exists
# -----------------------------------------

def is_supported_stock(symbol: str) -> bool:

    symbol = normalize_symbol(symbol)

    return symbol in STOCK_UNIVERSE


# -----------------------------------------
# Get stock information
# -----------------------------------------

def get_stock_info(symbol: str):

    symbol = normalize_symbol(symbol)

    return STOCK_UNIVERSE.get(symbol)


# -----------------------------------------
# Get company name
# -----------------------------------------

def get_company_name(symbol: str) -> str:

    info = get_stock_info(symbol)

    if not info:
        return "Unknown"

    return info.get(
        "company",
        "Unknown"
    )


# -----------------------------------------
# Get sector
# -----------------------------------------

def get_sector(symbol: str) -> str:

    info = get_stock_info(symbol)

    if not info:
        return "Unknown"

    return info.get(
        "sector",
        "Unknown"
    )


# -----------------------------------------
# Get complete universe
# -----------------------------------------

def get_all_stocks():

    return STOCK_UNIVERSE


# -----------------------------------------
# Get symbols only
# -----------------------------------------

def get_all_symbols():

    return list(
        STOCK_UNIVERSE.keys()
    )


# -----------------------------------------
# Get stocks by sector
# -----------------------------------------

def get_stocks_by_sector(sector: str):

    sector = sector.strip().lower()

    results = {}

    for symbol, info in STOCK_UNIVERSE.items():

        stock_sector = info.get(
            "sector",
            ""
        ).lower()

        if stock_sector == sector:

            results[symbol] = info

    return results