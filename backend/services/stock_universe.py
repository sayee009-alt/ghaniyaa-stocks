import json
from pathlib import Path
from datetime import datetime


# ============================================================
# GHANIYAA MASTER STOCK UNIVERSE
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"

MASTER_UNIVERSE_FILE = (
    DATABASE_DIR / "master_stock_universe.json"
)


# ============================================================
# ENSURE DATABASE DIRECTORY
# ============================================================

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD MASTER UNIVERSE
# ============================================================

def load_master_universe():

    if not MASTER_UNIVERSE_FILE.exists():

        return {
            "metadata": {
                "version": 1,
                "last_updated": None,
                "total_stocks": 0
            },
            "stocks": []
        }

    try:

        with open(
            MASTER_UNIVERSE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):

            return {
                "metadata": {
                    "version": 1,
                    "last_updated": None,
                    "total_stocks": 0
                },
                "stocks": []
            }

        return data

    except Exception as e:

        print(
            f"Master universe load error: {e}"
        )

        return {
            "metadata": {
                "version": 1,
                "last_updated": None,
                "total_stocks": 0
            },
            "stocks": []
        }


# ============================================================
# SAVE MASTER UNIVERSE
# ============================================================

def save_master_universe(stocks):

    stocks = list(stocks)

    stocks.sort(
        key=lambda stock: (
            stock.get("exchange", ""),
            stock.get("symbol", "")
        )
    )

    data = {

        "metadata": {

            "version": 1,

            "last_updated": (
                datetime.utcnow()
                .isoformat()
            ),

            "total_stocks": len(stocks)

        },

        "stocks": stocks

    }

    with open(
        MASTER_UNIVERSE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
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
    )


# ============================================================
# GET ALL STOCKS
# ============================================================

def get_master_universe():

    data = load_master_universe()

    return data.get(
        "stocks",
        []
    )


# ============================================================
# GET STOCK COUNT
# ============================================================

def get_master_universe_count():

    return len(
        get_master_universe()
    )


# ============================================================
# FIND STOCK
# ============================================================

def find_stock(
    symbol,
    exchange=None
):

    symbol = normalize_symbol(
        symbol
    )

    stocks = get_master_universe()

    for stock in stocks:

        if normalize_symbol(
            stock.get("symbol")
        ) != symbol:

            continue

        if exchange:

            if (
                stock.get("exchange", "")
                .upper()
                != exchange.upper()
            ):
                continue

        return stock

    return None


# ============================================================
# GET NSE STOCKS
# ============================================================

def get_nse_stocks():

    return [

        stock

        for stock in get_master_universe()

        if stock.get("exchange") == "NSE"

    ]


# ============================================================
# GET BSE STOCKS
# ============================================================

def get_bse_stocks():

    return [

        stock

        for stock in get_master_universe()

        if stock.get("exchange") == "BSE"

    ]


# ============================================================
# GET UNIQUE SYMBOLS
# ============================================================

def get_unique_symbols():

    symbols = set()

    for stock in get_master_universe():

        symbol = normalize_symbol(
            stock.get("symbol")
        )

        if symbol:

            symbols.add(symbol)

    return sorted(symbols)


# ============================================================
# ADD / UPDATE STOCK
# ============================================================

def upsert_stock(stock):

    symbol = normalize_symbol(
        stock.get("symbol")
    )

    exchange = (
        stock.get("exchange", "")
        .strip()
        .upper()
    )

    if not symbol or not exchange:

        return False

    stocks = get_master_universe()

    updated = False

    for index, existing in enumerate(stocks):

        existing_symbol = normalize_symbol(
            existing.get("symbol")
        )

        existing_exchange = (
            existing.get("exchange", "")
            .strip()
            .upper()
        )

        if (
            existing_symbol == symbol
            and existing_exchange == exchange
        ):

            stocks[index] = {
                **existing,
                **stock,
                "symbol": symbol,
                "exchange": exchange
            }

            updated = True

            break

    if not updated:

        stocks.append({

            **stock,

            "symbol": symbol,
            "exchange": exchange

        })

    save_master_universe(
        stocks
    )

    return True