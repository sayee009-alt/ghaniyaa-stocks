from backend.stock_universe import STOCK_UNIVERSE


# ============================================================
# GHANIYAA STOCK REGISTRY
# ============================================================
#
# STOCK_UNIVERSE is now loaded from:
#
# database/master_stock_universe.json
#
# The registry provides a stable interface for the rest of
# Ghaniyaa.
#
# ============================================================


# ============================================================
# NORMALIZE SYMBOL
# ============================================================

def normalize_symbol(symbol: str) -> str:

    if not symbol:
        return ""

    return (
        str(symbol)
        .strip()
        .upper()
        .replace(".NS", "")
        .replace(".BO", "")
    )


# ============================================================
# INTERNAL STOCK ITERATOR
# ============================================================

def _iter_stocks():

    for identity, stock in STOCK_UNIVERSE.items():

        if not isinstance(stock, dict):
            continue

        symbol = stock.get(
            "symbol"
        )

        if not symbol:
            continue

        yield (
            identity,
            stock
        )


# ============================================================
# BUILD UNIQUE SYMBOL MAP
# ============================================================

def _build_symbol_map():

    symbol_map = {}

    for identity, stock in _iter_stocks():

        symbol = normalize_symbol(
            stock.get("symbol")
        )

        if not symbol:
            continue

        # ----------------------------------------------------
        # If duplicate symbols exist, prefer the record that
        # contains NSE/BSE exchange information.
        # ----------------------------------------------------

        existing = symbol_map.get(
            symbol
        )

        if existing is None:

            symbol_map[symbol] = stock

            continue

        existing_exchanges = set(
            existing.get(
                "exchanges",
                []
            )
            if isinstance(
                existing.get("exchanges", []),
                list
            )
            else []
        )

        new_exchanges = set(
            stock.get(
                "exchanges",
                []
            )
            if isinstance(
                stock.get("exchanges", []),
                list
            )
            else []
        )

        if len(new_exchanges) > len(
            existing_exchanges
        ):

            symbol_map[symbol] = stock

    return symbol_map


# ============================================================
# CHECK WHETHER STOCK EXISTS
# ============================================================

def is_supported_stock(symbol: str) -> bool:

    symbol = normalize_symbol(
        symbol
    )

    if not symbol:
        return False

    symbol_map = _build_symbol_map()

    return symbol in symbol_map


# ============================================================
# GET STOCK INFORMATION
# ============================================================

def get_stock_info(symbol: str):

    symbol = normalize_symbol(
        symbol
    )

    if not symbol:
        return None

    symbol_map = _build_symbol_map()

    return symbol_map.get(
        symbol
    )


# ============================================================
# GET COMPANY NAME
# ============================================================

def get_company_name(symbol: str) -> str:

    info = get_stock_info(
        symbol
    )

    if not info:
        return "Unknown"

    return info.get(
        "company",
        "Unknown"
    )


# ============================================================
# GET SECTOR
# ============================================================

def get_sector(symbol: str) -> str:

    info = get_stock_info(
        symbol
    )

    if not info:
        return "Unknown"

    return info.get(
        "sector",
        "Unknown"
    )


# ============================================================
# GET COMPLETE MASTER UNIVERSE
# ============================================================

def get_all_stocks():

    return STOCK_UNIVERSE


# ============================================================
# GET UNIQUE SYMBOL MAP
# ============================================================

def get_all_symbol_map():

    return _build_symbol_map()


# ============================================================
# GET UNIQUE SYMBOLS
# ============================================================

def get_all_symbols():

    symbol_map = _build_symbol_map()

    return list(
        symbol_map.keys()
    )


# ============================================================
# MASTER RECORD COUNT
# ============================================================

def get_master_stock_count():

    return len(
        STOCK_UNIVERSE
    )


# ============================================================
# UNIQUE SYMBOL COUNT
# ============================================================

def get_unique_symbol_count():

    return len(
        _build_symbol_map()
    )


# ============================================================
# GET STOCKS BY SECTOR
# ============================================================

def get_stocks_by_sector(
    sector: str
):

    if not sector:
        return {}

    sector = (
        str(sector)
        .strip()
        .lower()
    )

    results = {}

    for symbol, stock in (
        _build_symbol_map().items()
    ):

        stock_sector = str(
            stock.get(
                "sector",
                ""
            )
        ).strip().lower()

        if stock_sector == sector:

            results[symbol] = stock

    return results


# ============================================================
# GET NSE STOCKS
# ============================================================

def get_nse_stocks():

    results = {}

    for symbol, stock in (
        _build_symbol_map().items()
    ):

        exchanges = stock.get(
            "exchanges",
            []
        )

        if isinstance(
            exchanges,
            str
        ):

            exchanges = [
                exchanges
            ]

        exchanges = {
            str(exchange)
            .upper()
            .strip()
            for exchange in exchanges
        }

        if "NSE" in exchanges:

            results[symbol] = stock

    return results


# ============================================================
# GET BSE STOCKS
# ============================================================

def get_bse_stocks():

    results = {}

    for symbol, stock in (
        _build_symbol_map().items()
    ):

        exchanges = stock.get(
            "exchanges",
            []
        )

        if isinstance(
            exchanges,
            str
        ):

            exchanges = [
                exchanges
            ]

        exchanges = {
            str(exchange)
            .upper()
            .strip()
            for exchange in exchanges
        }

        if "BSE" in exchanges:

            results[symbol] = stock

    return results