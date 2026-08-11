import json
from pathlib import Path
from datetime import datetime


# ============================================================
# GHANIYAA NSE + BSE MASTER UNIVERSE MERGER
# ============================================================
#
# Purpose:
#
# 1. Import NSE source records
# 2. Import BSE source records
# 3. Merge securities using ISIN as the primary identity
# 4. Preserve NSE and BSE identifiers
# 5. Preserve exchange membership
# 6. Write the final master universe
#
# Output:
#
# backend/database/master_stock_universe.json
#
# ============================================================


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = (
    BASE_DIR / "database"
)

MASTER_UNIVERSE_FILE = (
    DATABASE_DIR
    / "master_stock_universe.json"
)


# ============================================================
# DATABASE DIRECTORY
# ============================================================

def ensure_database_directory():

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# LOAD EXISTING MASTER UNIVERSE
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

    except Exception as error:

        print(
            f"Master universe load failed: {error}"
        )

        return {}


# ============================================================
# SAVE MASTER UNIVERSE
# ============================================================

def save_master_universe(
    universe
):

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
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    value
):

    if value is None:

        return ""

    return (
        str(value)
        .strip()
    )


# ============================================================
# NORMALIZE ISIN
# ============================================================

def normalize_isin(
    value
):

    if not value:

        return ""

    return (
        str(value)
        .strip()
        .upper()
    )


# ============================================================
# NORMALIZE SYMBOL
# ============================================================

def normalize_symbol(
    value
):

    if not value:

        return ""

    return (
        str(value)
        .strip()
        .upper()
        .replace(
            ".NS",
            ""
        )
        .replace(
            ".BO",
            ""
        )
    )


# ============================================================
# CREATE IDENTITY KEY
# ============================================================
#
# ISIN is the preferred identity.
#
# If ISIN is unavailable, we use an exchange-specific
# fallback so that unrelated securities are not accidentally
# merged.
#
# ============================================================

def get_identity_key(
    stock,
    source_exchange
):

    isin = normalize_isin(
        stock.get("isin")
    )

    if isin:

        return (
            f"ISIN:{isin}"
        )

    symbol = normalize_symbol(
        stock.get("symbol")
    )

    if not symbol:

        symbol = normalize_symbol(
            stock.get("scrip_id")
        )

    if not symbol:

        symbol = normalize_symbol(
            stock.get("bse_scrip_code")
        )

    return (
        f"{source_exchange.upper()}:{symbol}"
    )


# ============================================================
# ENSURE EXCHANGE LIST
# ============================================================

def normalize_exchanges(
    stock
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

    if not isinstance(
        exchanges,
        list
    ):

        exchanges = []

    exchange = normalize_text(
        stock.get(
            "exchange"
        )
    ).upper()

    result = []

    for item in exchanges:

        item = normalize_text(
            item
        ).upper()

        if item and item not in result:

            result.append(
                item
            )

    if exchange and exchange not in result:

        result.append(
            exchange
        )

    return result


# ============================================================
# MERGE ONE STOCK
# ============================================================

def merge_stock(
    universe,
    stock,
    source_exchange
):

    if not isinstance(
        stock,
        dict
    ):

        return False

    source_exchange = (
        source_exchange
        .strip()
        .upper()
    )

    if source_exchange not in {
        "NSE",
        "BSE"
    }:

        return False

    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    identity_key = get_identity_key(
        stock,
        source_exchange
    )

    # --------------------------------------------------------
    # Existing record
    # --------------------------------------------------------

    existing = universe.get(
        identity_key
    )

    if not isinstance(
        existing,
        dict
    ):

        existing = {}

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    isin = normalize_isin(
        stock.get(
            "isin"
        )
    )

    company = (
        normalize_text(
            stock.get(
                "company"
            )
        )
        or normalize_text(
            existing.get(
                "company"
            )
        )
        or "Unknown"
    )

    # --------------------------------------------------------
    # Preserve source identifiers
    # --------------------------------------------------------

    if source_exchange == "NSE":

        nse_symbol = normalize_symbol(
            stock.get(
                "symbol"
            )
        )

        if nse_symbol:

            existing[
                "nse_symbol"
            ] = nse_symbol

        if stock.get(
            "listing_date"
        ):

            existing[
                "nse_listing_date"
            ] = stock.get(
                "listing_date"
            )

        if stock.get(
            "series"
        ):

            existing[
                "nse_series"
            ] = stock.get(
                "series"
            )

        if stock.get(
            "paid_up_value"
        ):

            existing[
                "nse_paid_up_value"
            ] = stock.get(
                "paid_up_value"
            )

        if stock.get(
            "market_lot"
        ):

            existing[
                "nse_market_lot"
            ] = stock.get(
                "market_lot"
            )

        if stock.get(
            "face_value"
        ):

            existing[
                "nse_face_value"
            ] = stock.get(
                "face_value"
            )

        existing[
            "nse_yahoo_symbol"
        ] = (
            stock.get(
                "yahoo_symbol"
            )
            or (
                f"{nse_symbol}.NS"
                if nse_symbol
                else None
            )
        )

    # --------------------------------------------------------
    # BSE identifiers
    # --------------------------------------------------------

    if source_exchange == "BSE":

        bse_scrip_code = normalize_text(
            stock.get(
                "bse_scrip_code"
            )
        )

        bse_symbol = normalize_symbol(
            stock.get(
                "scrip_id"
            )
            or stock.get(
                "symbol"
            )
        )

        if bse_scrip_code:

            existing[
                "bse_scrip_code"
            ] = bse_scrip_code

        if bse_symbol:

            existing[
                "bse_symbol"
            ] = bse_symbol

        if stock.get(
            "security_name"
        ):

            existing[
                "bse_security_name"
            ] = stock.get(
                "security_name"
            )

        if stock.get(
            "status"
        ):

            existing[
                "bse_status"
            ] = stock.get(
                "status"
            )

        if stock.get(
            "group"
        ):

            existing[
                "bse_group"
            ] = stock.get(
                "group"
            )

        if stock.get(
            "face_value"
        ):

            existing[
                "bse_face_value"
            ] = stock.get(
                "face_value"
            )

        existing[
            "bse_yahoo_symbol"
        ] = (
            stock.get(
                "yahoo_symbol"
            )
            or (
                f"{bse_symbol}.BO"
                if bse_symbol
                else None
            )
        )

    # --------------------------------------------------------
    # Common fields
    # --------------------------------------------------------

    existing[
        "symbol"
    ] = (
        existing.get(
            "nse_symbol"
        )
        or existing.get(
            "bse_symbol"
        )
        or normalize_symbol(
            stock.get(
                "symbol"
            )
        )
        or existing.get(
            "symbol"
        )
    )

    existing[
        "company"
    ] = company

    if isin:

        existing[
            "isin"
        ] = isin

    # --------------------------------------------------------
    # Exchanges
    # --------------------------------------------------------

    exchanges = normalize_exchanges(
        existing
    )

    if source_exchange not in exchanges:

        exchanges.append(
            source_exchange
        )

    # Sort consistently
    exchanges = sorted(
        set(exchanges)
    )

    existing[
        "exchanges"
    ] = exchanges

    # Primary exchange
    #
    # Prefer NSE when available because NSE symbols are
    # generally the primary trading symbol used throughout
    # Ghaniyaa.

    if "NSE" in exchanges:

        existing[
            "exchange"
        ] = "NSE"

    elif "BSE" in exchanges:

        existing[
            "exchange"
        ] = "BSE"

    # --------------------------------------------------------
    # Active status
    # --------------------------------------------------------

    nse_active = (
        source_exchange == "NSE"
    )

    bse_active = (
        source_exchange == "BSE"
        and stock.get(
            "active",
            False
        )
    )

    if (
        nse_active
        or bse_active
        or existing.get(
            "active"
        )
    ):

        existing[
            "active"
        ] = True

        existing[
            "status"
        ] = "active"

    else:

        existing[
            "active"
        ] = False

        existing[
            "status"
        ] = "inactive"

    # --------------------------------------------------------
    # Sector
    # --------------------------------------------------------

    incoming_sector = normalize_text(
        stock.get(
            "sector"
        )
    )

    existing_sector = normalize_text(
        existing.get(
            "sector"
        )
    )

    if (
        incoming_sector
        and incoming_sector.lower()
        != "unknown"
    ):

        existing[
            "sector"
        ] = incoming_sector

    elif existing_sector:

        existing[
            "sector"
        ] = existing_sector

    else:

        existing[
            "sector"
        ] = "Unknown"

    # --------------------------------------------------------
    # Source tracking
    # --------------------------------------------------------

    sources = existing.get(
        "sources",
        []
    )

    if isinstance(
        sources,
        str
    ):

        sources = [
            sources
        ]

    if not isinstance(
        sources,
        list
    ):

        sources = []

    source_name = (
        "NSE India"
        if source_exchange == "NSE"
        else "BSE India"
    )

    if source_name not in sources:

        sources.append(
            source_name
        )

    existing[
        "sources"
    ] = sorted(
        set(sources)
    )

    # --------------------------------------------------------
    # Last updated
    # --------------------------------------------------------

    existing[
        "last_updated"
    ] = datetime.utcnow().isoformat()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    universe[
        identity_key
    ] = existing

    return True


# ============================================================
# MERGE NSE + BSE
# ============================================================

def merge_nse_bse_universe(
    nse_stocks=None,
    bse_stocks=None
):

    print(
        "Starting NSE + BSE universe merge..."
    )

    # ========================================================
    # LOAD SOURCES IF NOT PROVIDED
    # ========================================================

    if nse_stocks is None:

        from backend.services.nse_bse_importer import (
            import_nse_source
        )

        nse_stocks = (
            import_nse_source()
        )

    if bse_stocks is None:

        from backend.services.nse_bse_importer import (
            import_bse_source
        )

        bse_stocks = (
            import_bse_source()
        )

    # ========================================================
    # VALIDATE
    # ========================================================

    if not isinstance(
        nse_stocks,
        list
    ):

        nse_stocks = []

    if not isinstance(
        bse_stocks,
        list
    ):

        bse_stocks = []

    print(
        f"NSE source records: "
        f"{len(nse_stocks)}"
    )

    print(
        f"BSE source records: "
        f"{len(bse_stocks)}"
    )

    # ========================================================
    # NEW UNIVERSE
    # ========================================================
    #
    # We rebuild the exchange-derived portion from the source
    # data. This is important for future listing updates.
    #
    # ========================================================

    universe = {}

    # ========================================================
    # MERGE NSE
    # ========================================================

    nse_merged = 0

    for stock in nse_stocks:

        if merge_stock(
            universe,
            stock,
            "NSE"
        ):

            nse_merged += 1

    # ========================================================
    # MERGE BSE
    # ========================================================

    bse_merged = 0

    for stock in bse_stocks:

        if merge_stock(
            universe,
            stock,
            "BSE"
        ):

            bse_merged += 1

    # ========================================================
    # SAVE
    # ========================================================

    save_master_universe(
        universe
    )

    # ========================================================
    # COUNT EXCHANGE MEMBERSHIP
    # ========================================================

    nse_count = 0
    bse_count = 0
    both_count = 0

    active_count = 0
    inactive_count = 0

    for stock in universe.values():

        exchanges = stock.get(
            "exchanges",
            []
        )

        if "NSE" in exchanges:

            nse_count += 1

        if "BSE" in exchanges:

            bse_count += 1

        if (
            "NSE" in exchanges
            and "BSE" in exchanges
        ):

            both_count += 1

        if stock.get(
            "active",
            False
        ):

            active_count += 1

        else:

            inactive_count += 1

    # ========================================================
    # RESULT
    # ========================================================

    result = {

        "success": True,

        "nseSourceCount": len(
            nse_stocks
        ),

        "bseSourceCount": len(
            bse_stocks
        ),

        "nseMerged": nse_merged,

        "bseMerged": bse_merged,

        "masterCount": len(
            universe
        ),

        "nseStocks": nse_count,

        "bseStocks": bse_count,

        "bothExchanges": both_count,

        "activeStocks": active_count,

        "inactiveStocks": inactive_count,

        "file": str(
            MASTER_UNIVERSE_FILE
        ),

    }

    print(
        "NSE + BSE merge complete."
    )

    print(
        result
    )

    return result