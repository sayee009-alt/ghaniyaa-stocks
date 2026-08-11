from pathlib import Path
import json


# ============================================================
# GHANIYAA MARKET UNIVERSE
# ============================================================
#
# SOURCE OF TRUTH:
#
#     database/master_stock_universe.json
#
# This module must NOT use Yahoo Finance to discover or validate
# the complete stock universe.
#
# Yahoo Finance is a market-data provider, not our exchange
# security master.
#
# Architecture:
#
#     NSE/BSE Import
#          ↓
#     NSE + BSE Merge
#          ↓
#     master_stock_universe.json
#          ↓
#     this module
#          ↓
#     universe_sync.py
#
# ============================================================


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MASTER_UNIVERSE_FILE = (
    PROJECT_ROOT
    / "database"
    / "master_stock_universe.json"
)


# ============================================================
# SYMBOL NORMALIZATION
# ============================================================

def normalize_symbol(symbol: str) -> str:

    if not symbol:
        return ""

    symbol = (
        str(symbol)
        .strip()
        .upper()
    )

    # Remove Yahoo suffixes if somebody supplies one.
    for suffix in (
        ".NS",
        ".BO",
    ):
        if symbol.endswith(suffix):
            symbol = symbol[:-len(suffix)]

    return symbol


# ============================================================
# GET YAHOO SYMBOL
# ============================================================
#
# This helper is retained for downstream market-data services.
#
# It is NOT used for universe discovery.
# ============================================================

def get_yahoo_symbol(symbol: str) -> str:

    symbol = normalize_symbol(symbol)

    if not symbol:
        return ""

    return f"{symbol}.NS"


# ============================================================
# LOAD MASTER UNIVERSE
# ============================================================

def load_master_universe():

    if not MASTER_UNIVERSE_FILE.exists():

        raise FileNotFoundError(
            "Master stock universe not found: "
            f"{MASTER_UNIVERSE_FILE}"
        )

    try:

        with MASTER_UNIVERSE_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "Master stock universe contains invalid JSON: "
            f"{MASTER_UNIVERSE_FILE}"
        ) from exc

    if not isinstance(data, dict):

        raise RuntimeError(
            "Master stock universe must contain a JSON object."
        )

    return data


# ============================================================
# NORMALIZE MASTER RECORD
# ============================================================

def normalize_master_record(record):

    if not isinstance(record, dict):
        return None

    symbol = normalize_symbol(
        record.get("symbol")
    )

    if not symbol:
        return None

    exchanges = record.get(
        "exchanges",
        [],
    )

    if not isinstance(exchanges, list):
        exchanges = []

    exchanges = [
        str(exchange).strip().upper()
        for exchange in exchanges
        if exchange
    ]

    # Remove duplicates while preserving order.
    exchanges = list(
        dict.fromkeys(exchanges)
    )

    active = record.get(
        "active",
        True,
    )

    status = str(
        record.get(
            "status",
            "active" if active else "inactive",
        )
    ).strip().lower()

    return {
        **record,

        "symbol": symbol,

        "company": (
            record.get("company")
            or record.get("issuer_name")
            or record.get("security_name")
            or symbol
        ),

        "sector": (
            record.get("sector")
            or "Unknown"
        ),

        "exchanges": exchanges,

        "exchange": (
            record.get("exchange")
            or (
                "NSE"
                if "NSE" in exchanges
                else "BSE"
                if "BSE" in exchanges
                else (
                    exchanges[0]
                    if exchanges
                    else "UNKNOWN"
                )
            )
        ),

        "active": bool(active),

        "status": status,

        "yahoo_symbol": (
            record.get("yahoo_symbol")
            or record.get("nse_yahoo_symbol")
            or (
                f"{symbol}.NS"
                if "NSE" in exchanges
                else f"{symbol}.BO"
                if "BSE" in exchanges
                else ""
            )
        ),
    }


# ============================================================
# GET COMPLETE MASTER RECORDS
# ============================================================

def get_master_records(
    include_inactive: bool = True,
):

    raw_master = load_master_universe()

    records = []

    for record in raw_master.values():

        normalized = normalize_master_record(
            record
        )

        if not normalized:
            continue

        if (
            not include_inactive
            and not normalized.get("active", True)
        ):
            continue

        records.append(normalized)

    return records


# ============================================================
# GET NSE EQUITY UNIVERSE
# ============================================================

def get_nse_equity_universe():

    records = get_master_records(
        include_inactive=False
    )

    results = []

    seen = set()

    for stock in records:

        symbol = normalize_symbol(
            stock.get("symbol")
        )

        if not symbol:
            continue

        exchanges = {
            str(exchange).upper()
            for exchange in stock.get(
                "exchanges",
                [],
            )
        }

        # A stock belongs to NSE if the master says NSE.
        #
        # We do NOT ask Yahoo whether it exists.
        if "NSE" not in exchanges:
            continue

        if symbol in seen:
            continue

        seen.add(symbol)

        results.append({

            **stock,

            "symbol": symbol,

            "exchange": "NSE",

            "yahoo_symbol": (
                stock.get("nse_yahoo_symbol")
                or f"{symbol}.NS"
            ),
        })

    return results


# ============================================================
# GET BSE EQUITY UNIVERSE
# ============================================================

def get_bse_equity_universe():

    records = get_master_records(
        include_inactive=False
    )

    results = []

    seen = set()

    for stock in records:

        symbol = normalize_symbol(
            stock.get("symbol")
        )

        if not symbol:
            continue

        exchanges = {
            str(exchange).upper()
            for exchange in stock.get(
                "exchanges",
                [],
            )
        }

        if "BSE" not in exchanges:
            continue

        if symbol in seen:
            continue

        seen.add(symbol)

        results.append({

            **stock,

            "symbol": symbol,

            "exchange": "BSE",

            "yahoo_symbol": (
                stock.get("bse_yahoo_symbol")
                or f"{symbol}.BO"
            ),
        })

    return results


# ============================================================
# GET COMPLETE EQUITY UNIVERSE
# ============================================================

def get_equity_universe():

    records = get_master_records(
        include_inactive=False
    )

    results = []

    seen = set()

    for stock in records:

        symbol = normalize_symbol(
            stock.get("symbol")
        )

        if not symbol:
            continue

        if symbol in seen:
            continue

        seen.add(symbol)

        results.append(stock)

    return results


# ============================================================
# GET MARKET UNIVERSE
# ============================================================
#
# IMPORTANT:
#
# This function returns the master universe directly.
#
# NO Yahoo Finance calls.
# ============================================================

def get_market_universe():

    return get_equity_universe()


# ============================================================
# GET MARKET SYMBOLS
# ============================================================

def get_market_symbols():

    return [
        stock["symbol"]
        for stock in get_market_universe()
        if stock.get("symbol")
    ]


# ============================================================
# VALIDATE ONE MASTER RECORD
# ============================================================
#
# This is structural validation only.
#
# It deliberately does NOT contact Yahoo Finance.
# ============================================================

def validate_market_record(stock):

    if not isinstance(stock, dict):

        return {
            "symbol": "",
            "valid": False,
            "reason": "Record is not an object",
        }

    symbol = normalize_symbol(
        stock.get("symbol")
    )

    if not symbol:

        return {
            "symbol": "",
            "valid": False,
            "reason": "Missing symbol",
        }

    company = (
        stock.get("company")
        or stock.get("issuer_name")
        or stock.get("security_name")
    )

    if not company:

        return {
            "symbol": symbol,
            "valid": False,
            "reason": "Missing company name",
        }

    exchanges = stock.get(
        "exchanges",
        [],
    )

    if not isinstance(exchanges, list):

        return {
            "symbol": symbol,
            "valid": False,
            "reason": "Invalid exchanges field",
        }

    exchanges = [
        str(exchange).strip().upper()
        for exchange in exchanges
        if exchange
    ]

    if not exchanges:

        return {
            "symbol": symbol,
            "valid": False,
            "reason": "Missing exchange information",
        }

    if not any(
        exchange in ("NSE", "BSE")
        for exchange in exchanges
    ):

        return {
            "symbol": symbol,
            "valid": False,
            "reason": "Not an NSE/BSE security",
        }

    return {

        "symbol": symbol,

        "valid": True,

        "company": company,

        "exchanges": exchanges,

        "active": stock.get(
            "active",
            True,
        ),
    }


# ============================================================
# VALIDATE COMPLETE MARKET UNIVERSE
# ============================================================
#
# Structural validation only.
#
# NO Yahoo Finance.
# ============================================================

def validate_market_universe():

    records = get_master_records(
        include_inactive=False
    )

    results = []

    for stock in records:

        results.append(
            validate_market_record(
                stock
            )
        )

    return results


# ============================================================
# GET MARKET VALIDATION REPORT
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

        "stocks": results,

        "source": str(
            MASTER_UNIVERSE_FILE
        ),

        "validation_type": "master-record-structural",
    }