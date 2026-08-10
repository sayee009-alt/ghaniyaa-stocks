from datetime import datetime

from backend.stock_universe import STOCK_UNIVERSE

from backend.services.market_universe import (
    get_market_universe,
    get_market_validation_report,
)


# ============================================================
# GHANIYAA UNIVERSE SYNCHRONIZATION
# ============================================================
#
# Purpose:
#
# Market universe
#       ↓
# Validate
#       ↓
# Add valid stocks
#       ↓
# Preserve existing stocks
#
# IMPORTANT:
#
# We do NOT delete stocks from STOCK_UNIVERSE automatically.
#
# A temporary Yahoo failure should never cause Ghaniyaa to
# accidentally remove a company from its research universe.
#
# ============================================================


def sync_stock_universe():

    # --------------------------------------------------------
    # Get currently valid market stocks
    # --------------------------------------------------------

    market_stocks = get_market_universe()

    added = 0

    existing = 0

    skipped = 0

    now = datetime.utcnow().isoformat()

    # --------------------------------------------------------
    # Add valid market stocks to Ghaniyaa registry
    # --------------------------------------------------------

    for stock in market_stocks:

        symbol = stock.get(
            "symbol"
        )

        if not symbol:

            skipped += 1

            continue

        symbol = (
            symbol
            .strip()
            .upper()
        )

        company = stock.get(
            "company",
            symbol
        )

        sector = stock.get(
            "sector",
            "Unknown"
        )

        exchange = stock.get(
            "exchange",
            "NSI"
        )

        yahoo_symbol = stock.get(
            "yahoo_symbol",
            symbol + ".NS"
        )

        # ----------------------------------------------------
        # Existing stock
        # ----------------------------------------------------

        if symbol in STOCK_UNIVERSE:

            existing += 1

            # Preserve existing information.
            #
            # Only fill missing fields.

            current = STOCK_UNIVERSE[symbol]

            if not current.get("company"):
                current["company"] = company

            if not current.get("sector"):
                current["sector"] = sector

            if not current.get("exchange"):
                current["exchange"] = exchange

            if not current.get("yahoo_symbol"):
                current["yahoo_symbol"] = yahoo_symbol

            current["last_verified"] = now

            current["status"] = "active"

            continue

        # ----------------------------------------------------
        # New stock
        # ----------------------------------------------------

        STOCK_UNIVERSE[symbol] = {

            "company": company,

            "sector": sector,

            "exchange": exchange,

            "yahoo_symbol": yahoo_symbol,

            "status": "active",

            "first_seen": now,

            "last_verified": now
        }

        added += 1

    # --------------------------------------------------------
    # Validation report
    # --------------------------------------------------------

    report = get_market_validation_report()

    invalid_symbols = []

    for stock in report.get(
        "stocks",
        []
    ):

        if stock.get("valid") is False:

            invalid_symbols.append({

                "symbol": stock.get(
                    "symbol"
                ),

                "reason": stock.get(
                    "reason",
                    "Unknown"
                )
            })

    # --------------------------------------------------------
    # Return synchronization summary
    # --------------------------------------------------------

    return {

        "market_stocks": report.get(
            "total",
            0
        ),

        "valid_market_stocks": report.get(
            "valid",
            0
        ),

        "invalid_market_stocks": report.get(
            "invalid",
            0
        ),

        "ghaniyaa_stocks": len(
            STOCK_UNIVERSE
        ),

        "added": added,

        "existing": existing,

        "skipped": skipped,

        "invalid_symbols": invalid_symbols,

        "synced_at": now
    }