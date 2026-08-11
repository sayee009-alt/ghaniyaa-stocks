from datetime import datetime, timezone

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
# Synchronize the validated NSE + BSE market universe into the
# Ghaniyaa application registry WITHOUT creating duplicates.
#
# IMPORTANT:
#
# master_stock_universe.json uses identity keys such as:
#
#     ISIN:INE144J01027
#
# while application lookups normally use:
#
#     TCS
#     INFY
#     RELIANCE
#
# Therefore we MUST NOT do:
#
#     if symbol in STOCK_UNIVERSE:
#
# because the dictionary key is NOT necessarily the symbol.
#
# Instead we build indexes from the actual records.
#
# ============================================================


# ============================================================
# NORMALIZE TEXT
# ============================================================

def _normalize(value):
    if value is None:
        return ""

    return str(value).strip().upper()


# ============================================================
# BUILD EXISTING STOCK INDEXES
# ============================================================

def _build_existing_indexes():

    symbol_index = {}
    isin_index = {}
    yahoo_index = {}

    for key, record in STOCK_UNIVERSE.items():

        if not isinstance(record, dict):
            continue

        # ----------------------------------------------------
        # Symbol
        # ----------------------------------------------------

        symbol = _normalize(
            record.get("symbol")
        )

        if symbol:
            symbol_index[symbol] = key

        # ----------------------------------------------------
        # ISIN
        # ----------------------------------------------------

        isin = _normalize(
            record.get("isin")
        )

        if isin:
            isin_index[isin] = key

        # ----------------------------------------------------
        # NSE Yahoo symbol
        # ----------------------------------------------------

        nse_yahoo = _normalize(
            record.get("nse_yahoo_symbol")
        )

        if nse_yahoo:
            yahoo_index[nse_yahoo] = key

        # ----------------------------------------------------
        # BSE Yahoo symbol
        # ----------------------------------------------------

        bse_yahoo = _normalize(
            record.get("bse_yahoo_symbol")
        )

        if bse_yahoo:
            yahoo_index[bse_yahoo] = key

        # ----------------------------------------------------
        # Generic Yahoo symbol
        # ----------------------------------------------------

        yahoo_symbol = _normalize(
            record.get("yahoo_symbol")
        )

        if yahoo_symbol:
            yahoo_index[yahoo_symbol] = key

    return (
        symbol_index,
        isin_index,
        yahoo_index,
    )


# ============================================================
# FIND EXISTING RECORD
# ============================================================

def _find_existing_record(
    stock,
    symbol_index,
    isin_index,
    yahoo_index,
):

    symbol = _normalize(
        stock.get("symbol")
    )

    isin = _normalize(
        stock.get("isin")
    )

    yahoo_symbol = _normalize(
        stock.get("yahoo_symbol")
    )

    # --------------------------------------------------------
    # 1. ISIN is the strongest identity
    # --------------------------------------------------------

    if isin and isin in isin_index:

        return isin_index[isin]

    # --------------------------------------------------------
    # 2. Symbol
    # --------------------------------------------------------

    if symbol and symbol in symbol_index:

        return symbol_index[symbol]

    # --------------------------------------------------------
    # 3. Yahoo symbol
    # --------------------------------------------------------

    if yahoo_symbol and yahoo_symbol in yahoo_index:

        return yahoo_index[yahoo_symbol]

    # --------------------------------------------------------
    # 4. NSE Yahoo symbol
    # --------------------------------------------------------

    nse_yahoo = _normalize(
        stock.get("nse_yahoo_symbol")
    )

    if nse_yahoo and nse_yahoo in yahoo_index:

        return yahoo_index[nse_yahoo]

    # --------------------------------------------------------
    # 5. BSE Yahoo symbol
    # --------------------------------------------------------

    bse_yahoo = _normalize(
        stock.get("bse_yahoo_symbol")
    )

    if bse_yahoo and bse_yahoo in yahoo_index:

        return yahoo_index[bse_yahoo]

    return None


# ============================================================
# UPDATE EXISTING RECORD
# ============================================================

def _update_existing_record(
    current,
    incoming,
    now,
):

    if not isinstance(current, dict):
        return

    # --------------------------------------------------------
    # Fields that should be refreshed when available
    # --------------------------------------------------------

    fields = [
        "symbol",
        "company",
        "isin",
        "exchange",
        "exchanges",
        "active",
        "status",
        "sector",
        "sources",
        "yahoo_symbol",

        # NSE
        "nse_symbol",
        "nse_listing_date",
        "nse_series",
        "nse_paid_up_value",
        "nse_market_lot",
        "nse_face_value",
        "nse_yahoo_symbol",

        # BSE
        "bse_scrip_code",
        "bse_symbol",
        "bse_security_name",
        "bse_status",
        "bse_group",
        "bse_face_value",
        "bse_yahoo_symbol",
    ]

    for field in fields:

        value = incoming.get(field)

        if value is None:
            continue

        if value == "":
            continue

        current[field] = value

    # --------------------------------------------------------
    # Preserve/update timestamp
    # --------------------------------------------------------

    current["last_verified"] = now
    current["last_updated"] = now


# ============================================================
# CREATE NEW RECORD
# ============================================================

def _create_new_record(stock, now):

    record = dict(stock)

    record.setdefault(
        "status",
        "active"
    )

    record.setdefault(
        "active",
        True
    )

    record.setdefault(
        "first_seen",
        now
    )

    record["last_verified"] = now
    record["last_updated"] = now

    return record


# ============================================================
# GENERATE SAFE KEY
# ============================================================

def _generate_new_key(stock):

    isin = _normalize(
        stock.get("isin")
    )

    if isin:
        return f"ISIN:{isin}"

    symbol = _normalize(
        stock.get("symbol")
    )

    if symbol:
        return f"SYMBOL:{symbol}"

    yahoo_symbol = _normalize(
        stock.get("yahoo_symbol")
    )

    if yahoo_symbol:
        return f"YAHOO:{yahoo_symbol}"

    return ""


# ============================================================
# MAIN SYNCHRONIZATION
# ============================================================

def sync_stock_universe():

    print(
        "\nGHANIYAA UNIVERSE SYNCHRONIZATION"
    )

    print(
        "Loading validated market universe..."
    )

    market_stocks = get_market_universe()

    print(
        f"Validated market stocks: {len(market_stocks)}"
    )

    # --------------------------------------------------------
    # Build indexes from existing 8018 master records
    # --------------------------------------------------------

    (
        symbol_index,
        isin_index,
        yahoo_index,
    ) = _build_existing_indexes()

    print(
        f"Existing master records: {len(STOCK_UNIVERSE)}"
    )

    print(
        f"Existing symbol index: {len(symbol_index)}"
    )

    print(
        f"Existing ISIN index: {len(isin_index)}"
    )

    # --------------------------------------------------------
    # Counters
    # --------------------------------------------------------

    added = 0
    existing = 0
    updated = 0
    skipped = 0

    now = datetime.now(
        timezone.utc
    ).isoformat()

    added_symbols = []
    updated_symbols = []
    skipped_symbols = []

    # --------------------------------------------------------
    # Process market universe
    # --------------------------------------------------------

    for stock in market_stocks:

        if not isinstance(stock, dict):

            skipped += 1

            continue

        symbol = _normalize(
            stock.get("symbol")
        )

        if not symbol:

            skipped += 1

            skipped_symbols.append({
                "symbol": "",
                "reason": "Missing symbol",
            })

            continue

        # ----------------------------------------------------
        # Find existing record using ISIN / symbol / Yahoo
        # ----------------------------------------------------

        existing_key = _find_existing_record(
            stock,
            symbol_index,
            isin_index,
            yahoo_index,
        )

        # ----------------------------------------------------
        # Existing stock
        # ----------------------------------------------------

        if existing_key is not None:

            existing += 1

            current = STOCK_UNIVERSE.get(
                existing_key
            )

            if not isinstance(current, dict):

                skipped += 1

                skipped_symbols.append({
                    "symbol": symbol,
                    "reason": (
                        "Existing registry entry is not a dictionary"
                    ),
                })

                continue

            # Save snapshot before update
            before = dict(current)

            _update_existing_record(
                current,
                stock,
                now,
            )

            # Determine whether actual data changed
            changed = False

            for key in current:

                if key in (
                    "last_verified",
                    "last_updated",
                ):
                    continue

                if before.get(key) != current.get(key):

                    changed = True

                    break

            if changed:

                updated += 1

                updated_symbols.append(
                    symbol
                )

            # ------------------------------------------------
            # Keep indexes current
            # ------------------------------------------------

            symbol_index[symbol] = existing_key

            isin = _normalize(
                current.get("isin")
            )

            if isin:
                isin_index[isin] = existing_key

            for yahoo_field in (
                "yahoo_symbol",
                "nse_yahoo_symbol",
                "bse_yahoo_symbol",
            ):

                yahoo = _normalize(
                    current.get(yahoo_field)
                )

                if yahoo:

                    yahoo_index[yahoo] = existing_key

            continue

        # ----------------------------------------------------
        # New stock
        # ----------------------------------------------------

        new_key = _generate_new_key(
            stock
        )

        if not new_key:

            skipped += 1

            skipped_symbols.append({
                "symbol": symbol,
                "reason": "Unable to generate identity key",
            })

            continue

        # ----------------------------------------------------
        # Extremely defensive duplicate check
        # ----------------------------------------------------

        if new_key in STOCK_UNIVERSE:

            existing += 1

            current = STOCK_UNIVERSE[
                new_key
            ]

            if isinstance(current, dict):

                _update_existing_record(
                    current,
                    stock,
                    now,
                )

            continue

        # ----------------------------------------------------
        # Add new record
        # ----------------------------------------------------

        STOCK_UNIVERSE[new_key] = (
            _create_new_record(
                stock,
                now,
            )
        )

        added += 1

        added_symbols.append(
            symbol
        )

        # ----------------------------------------------------
        # Update indexes
        # ----------------------------------------------------

        symbol_index[symbol] = new_key

        isin = _normalize(
            stock.get("isin")
        )

        if isin:
            isin_index[isin] = new_key

        for yahoo_field in (
            "yahoo_symbol",
            "nse_yahoo_symbol",
            "bse_yahoo_symbol",
        ):

            yahoo = _normalize(
                stock.get(yahoo_field)
            )

            if yahoo:

                yahoo_index[yahoo] = new_key

    # ========================================================
    # VALIDATION REPORT
    # ========================================================

    report = get_market_validation_report()

    invalid_symbols = []

    for stock in report.get(
        "stocks",
        [],
    ):

        if stock.get("valid") is False:

            invalid_symbols.append({
                "symbol": stock.get(
                    "symbol"
                ),
                "reason": stock.get(
                    "reason",
                    "Unknown",
                ),
            })

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    final_count = len(
        STOCK_UNIVERSE
    )

    print(
        "\nGHANIYAA UNIVERSE SYNC COMPLETE"
    )

    print(
        f"Market records: {len(market_stocks)}"
    )

    print(
        f"Existing: {existing}"
    )

    print(
        f"Updated: {updated}"
    )

    print(
        f"Added: {added}"
    )

    print(
        f"Skipped: {skipped}"
    )

    print(
        f"Final registry count: {final_count}"
    )

    return {

        "market_stocks": report.get(
            "total",
            len(market_stocks),
        ),

        "valid_market_stocks": report.get(
            "valid",
            len(market_stocks),
        ),

        "invalid_market_stocks": report.get(
            "invalid",
            0,
        ),

        "ghaniyaa_stocks": final_count,

        "added": added,

        "existing": existing,

        "updated": updated,

        "skipped": skipped,

        "invalid_symbols": invalid_symbols,

        "added_symbols": added_symbols,

        "updated_symbols": updated_symbols,

        "skipped_symbols": skipped_symbols,

        "synced_at": now,
    }