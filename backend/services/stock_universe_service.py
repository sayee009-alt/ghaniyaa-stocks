import json
from pathlib import Path
from datetime import datetime

import yfinance as yf


# ============================================================
# GHANIYAA MASTER STOCK UNIVERSE SERVICE
# ============================================================
#
# Purpose:
#
# 1. Maintain the master NSE + BSE stock universe
# 2. Read the current registry
# 3. Discover/update stock listings
# 4. Normalize stock information
# 5. Save the updated universe
#
# This service is designed so the rest of Ghaniyaa can use
# one central stock universe.
#
# ============================================================


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"

MASTER_UNIVERSE_FILE = (
    DATABASE_DIR / "master_stock_universe.json"
)


# ============================================================
# ENSURE DATABASE DIRECTORY
# ============================================================

def ensure_database_directory():
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# LOAD MASTER UNIVERSE
# ============================================================

def load_master_universe():

    ensure_database_directory()

    if not MASTER_UNIVERSE_FILE.exists():

        return {}

    try:

        with open(
            MASTER_UNIVERSE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):

                return data

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ) as error:

        print(
            f"Master universe load error: {error}"
        )

        return {}


# ============================================================
# SAVE MASTER UNIVERSE
# ============================================================

def save_master_universe(universe):

    ensure_database_directory()

    with open(
        MASTER_UNIVERSE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            universe,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# NORMALIZE SYMBOL
# ============================================================

def normalize_symbol(symbol):

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
# NORMALIZE STOCK
# ============================================================

def normalize_stock(
    symbol,
    company=None,
    sector=None,
    exchange=None,
    yahoo_symbol=None
):

    symbol = normalize_symbol(symbol)

    if not symbol:
        return None

    return {

        "symbol": symbol,

        "company": (
            company
            or symbol
        ),

        "sector": (
            sector
            or "Unknown"
        ),

        "exchange": (
            exchange
            or "NSE"
        ),

        "yahoo_symbol": (
            yahoo_symbol
            or f"{symbol}.NS"
        ),

        "last_updated": (
            datetime.utcnow()
            .isoformat()
        )

    }


# ============================================================
# ADD / UPDATE STOCK
# ============================================================

def add_or_update_stock(
    symbol,
    company=None,
    sector=None,
    exchange=None,
    yahoo_symbol=None
):

    universe = load_master_universe()

    stock = normalize_stock(
        symbol=symbol,
        company=company,
        sector=sector,
        exchange=exchange,
        yahoo_symbol=yahoo_symbol
    )

    if not stock:
        return False

    universe[stock["symbol"]] = stock

    save_master_universe(universe)

    return True


# ============================================================
# GET ALL MASTER STOCKS
# ============================================================

def get_master_universe():

    return load_master_universe()


# ============================================================
# GET ALL SYMBOLS
# ============================================================

def get_master_symbols():

    universe = load_master_universe()

    return list(
        universe.keys()
    )


# ============================================================
# GET STOCK
# ============================================================

def get_master_stock(symbol):

    symbol = normalize_symbol(symbol)

    universe = load_master_universe()

    return universe.get(symbol)


# ============================================================
# CHECK STOCK
# ============================================================

def is_master_stock(symbol):

    symbol = normalize_symbol(symbol)

    universe = load_master_universe()

    return symbol in universe


# ============================================================
# YAHOO SYMBOL CANDIDATES
# ============================================================

def yahoo_symbol_candidates(symbol):

    symbol = normalize_symbol(symbol)

    return [
        f"{symbol}.NS",
        f"{symbol}.BO"
    ]


# ============================================================
# FETCH STOCK INFORMATION
# ============================================================

def fetch_stock_information(symbol):

    symbol = normalize_symbol(symbol)

    if not symbol:
        return None

    for yahoo_symbol in yahoo_symbol_candidates(symbol):

        try:

            ticker = yf.Ticker(
                yahoo_symbol
            )

            info = ticker.info

            if not info:
                continue

            company = (
                info.get("longName")
                or info.get("shortName")
                or symbol
            )

            sector = (
                info.get("sector")
                or "Unknown"
            )

            exchange = (
                info.get("exchange")
                or ""
            )

            return {

                "symbol": symbol,

                "company": company,

                "sector": sector,

                "exchange": exchange,

                "yahoo_symbol": yahoo_symbol,

                "last_updated": (
                    datetime.utcnow()
                    .isoformat()
                )

            }

        except Exception as error:

            print(
                f"Yahoo lookup failed "
                f"for {yahoo_symbol}: {error}"
            )

            continue

    return None


# ============================================================
# DISCOVER STOCK
# ============================================================

def discover_stock(symbol):

    symbol = normalize_symbol(symbol)

    if not symbol:
        return None

    existing = get_master_stock(
        symbol
    )

    if existing:

        return existing

    discovered = fetch_stock_information(
        symbol
    )

    if not discovered:
        return None

    add_or_update_stock(
        symbol=discovered["symbol"],
        company=discovered["company"],
        sector=discovered["sector"],
        exchange=discovered["exchange"],
        yahoo_symbol=discovered["yahoo_symbol"]
    )

    return discovered


# ============================================================
# UPDATE EXISTING STOCK
# ============================================================

def update_stock(symbol):

    symbol = normalize_symbol(symbol)

    if not symbol:
        return None

    discovered = fetch_stock_information(
        symbol
    )

    if not discovered:
        return None

    add_or_update_stock(
        symbol=discovered["symbol"],
        company=discovered["company"],
        sector=discovered["sector"],
        exchange=discovered["exchange"],
        yahoo_symbol=discovered["yahoo_symbol"]
    )

    return discovered


# ============================================================
# UPDATE ENTIRE MASTER UNIVERSE
# ============================================================

def update_master_universe():

    universe = load_master_universe()

    updated = []

    failed = []

    for symbol in list(
        universe.keys()
    ):

        result = update_stock(
            symbol
        )

        if result:

            updated.append(
                symbol
            )

        else:

            failed.append(
                symbol
            )

    return {

        "updated": updated,

        "updatedCount": len(
            updated
        ),

        "failed": failed,

        "failedCount": len(
            failed
        ),

        "total": len(
            universe
        )

    }


# ============================================================
# IMPORT EXISTING STOCK UNIVERSE
# ============================================================
#
# This imports the current hard-coded STOCK_UNIVERSE so we
# don't lose the stocks already registered in Ghaniyaa.
#
# ============================================================

def import_existing_universe():

    try:

        from backend.stock_universe import STOCK_UNIVERSE

    except Exception as error:

        print(
            f"Unable to import STOCK_UNIVERSE: {error}"
        )

        return {

            "imported": 0,

            "failed": 0

        }

    universe = load_master_universe()

    imported = 0

    for symbol, info in STOCK_UNIVERSE.items():

        symbol = normalize_symbol(
            symbol
        )

        if not symbol:
            continue

        company = (
            info.get(
                "company"
            )
            if isinstance(
                info,
                dict
            )
            else None
        )

        sector = (
            info.get(
                "sector"
            )
            if isinstance(
                info,
                dict
            )
            else None
        )

        exchange = (
            info.get(
                "exchange"
            )
            if isinstance(
                info,
                dict
            )
            else "NSE"
        )

        yahoo_symbol = (
            info.get(
                "yahoo_symbol"
            )
            if isinstance(
                info,
                dict
            )
            else None
        )

        stock = normalize_stock(
            symbol=symbol,
            company=company,
            sector=sector,
            exchange=exchange,
            yahoo_symbol=yahoo_symbol
        )

        if stock:

            universe[symbol] = stock

            imported += 1

    save_master_universe(
        universe
    )

    return {

        "imported": imported,

        "failed": 0

    }


# ============================================================
# UNIVERSE SUMMARY
# ============================================================

def get_universe_summary():
    """
    Return a safe summary of the master stock universe.

    Supports both dictionary-based and list-based
    master-universe structures.
    """

    universe = load_master_universe()

    # =========================================================
    # NORMALIZE UNIVERSE
    # =========================================================

    stocks = []

    if isinstance(universe, dict):

        for symbol, value in universe.items():

            if isinstance(value, dict):

                stock = dict(value)

                stock.setdefault(
                    "symbol",
                    symbol
                )

                stocks.append(stock)

    elif isinstance(universe, list):

        for value in universe:

            if isinstance(value, dict):

                stocks.append(value)

    # =========================================================
    # COUNTERS
    # =========================================================

    total_stocks = len(stocks)

    nse_stocks = 0
    bse_stocks = 0

    active_stocks = 0
    inactive_stocks = 0

    sectors = {}

    # =========================================================
    # ANALYZE STOCKS
    # =========================================================

    for stock in stocks:

        if not isinstance(stock, dict):
            continue

        # -----------------------------------------------------
        # Exchange
        # -----------------------------------------------------

        exchange = str(
            stock.get(
                "exchange",
                ""
            )
        ).upper().strip()

        exchanges = stock.get(
            "exchanges",
            []
        )

        if isinstance(exchanges, str):

            exchanges = [
                exchanges
            ]

        if not isinstance(exchanges, list):

            exchanges = []

        exchange_set = {
            str(item).upper().strip()
            for item in exchanges
        }

        # Support either:
        #
        # exchange: "NSE"
        #
        # or:
        #
        # exchanges: ["NSE", "BSE"]

        if exchange:
            exchange_set.add(exchange)

        if "NSE" in exchange_set:
            nse_stocks += 1

        if "BSE" in exchange_set:
            bse_stocks += 1

        # -----------------------------------------------------
        # Sector
        # -----------------------------------------------------

        sector = stock.get(
            "sector",
            "Unknown"
        )

        if sector is None:
            sector = "Unknown"

        sector = str(
            sector
        ).strip()

        if not sector:
            sector = "Unknown"

        sectors[sector] = (
            sectors.get(sector, 0) + 1
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        status = str(
            stock.get(
                "status",
                "active"
            )
        ).lower().strip()

        if status == "active":
            active_stocks += 1

        else:
            inactive_stocks += 1

    # =========================================================
    # RETURN SUMMARY
    # =========================================================

    return {
        "totalStocks": total_stocks,

        "nseStocks": nse_stocks,

        "bseStocks": bse_stocks,

        "activeStocks": active_stocks,

        "inactiveStocks": inactive_stocks,

        "sectorCount": len(
            sectors
        ),

        "sectors": sectors,
    }