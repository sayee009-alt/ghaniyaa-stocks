import json
from pathlib import Path
from datetime import datetime


# ============================================================
# GHANIYAA MASTER STOCK UNIVERSE REFRESH SERVICE
# ============================================================
#
# Purpose:
#
# 1. Download the latest NSE universe
# 2. Load the latest BSE universe
# 3. Merge both sources
# 4. Compare with the previous master universe
# 5. Detect new stocks
# 6. Detect removed/inactive stocks
# 7. Preserve the master universe
# 8. Save a refresh report
#
# ============================================================


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"

MASTER_UNIVERSE_FILE = (
    DATABASE_DIR / "master_stock_universe.json"
)

REFRESH_REPORT_FILE = (
    DATABASE_DIR / "stock_universe_refresh_report.json"
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
# LOAD JSON
# ============================================================

def load_json_file(
    path
):

    if not path.exists():

        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"Unable to load {path}: {error}"
        )

        return {}


# ============================================================
# SAVE JSON
# ============================================================

def save_json_file(
    path,
    data
):

    ensure_database_directory()

    with open(
        path,
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
# LOAD MASTER
# ============================================================

def load_previous_master():

    data = load_json_file(
        MASTER_UNIVERSE_FILE
    )

    if not isinstance(
        data,
        dict
    ):

        return {}

    return data


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
# GET MASTER IDENTITY
# ============================================================
#
# The merger uses:
#
#     ISIN:<ISIN>
#
# when ISIN exists.
#
# Otherwise it uses an exchange-specific fallback.
#
# ============================================================

def get_identity(
    stock
):

    if not isinstance(
        stock,
        dict
    ):

        return ""

    key = stock.get(
        "key"
    )

    if key:

        return str(
            key
        )

    isin = normalize_isin(
        stock.get(
            "isin"
        )
    )

    if isin:

        return (
            f"ISIN:{isin}"
        )

    symbol = (
        stock.get(
            "nse_symbol"
        )
        or stock.get(
            "bse_symbol"
        )
        or stock.get(
            "symbol"
        )
    )

    if not symbol:

        return ""

    symbol = (
        str(symbol)
        .strip()
        .upper()
    )

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

    if (
        isinstance(
            exchanges,
            list
        )
        and exchanges
    ):

        exchange = (
            str(
                exchanges[0]
            )
            .strip()
            .upper()
        )

    else:

        exchange = "UNKNOWN"

    return (
        f"{exchange}:{symbol}"
    )


# ============================================================
# NORMALIZE MASTER INDEX
# ============================================================

def build_master_index(
    universe
):

    index = {}

    if not isinstance(
        universe,
        dict
    ):

        return index

    for key, stock in universe.items():

        if not isinstance(
            stock,
            dict
        ):

            continue

        identity = (
            str(key)
            if key
            else get_identity(
                stock
            )
        )

        if identity:

            index[
                identity
            ] = stock

    return index


# ============================================================
# DETECT CHANGES
# ============================================================

def compare_universes(
    previous,
    current
):

    previous_index = (
        build_master_index(
            previous
        )
    )

    current_index = (
        build_master_index(
            current
        )
    )

    previous_keys = set(
        previous_index.keys()
    )

    current_keys = set(
        current_index.keys()
    )

    # --------------------------------------------------------
    # New stocks
    # --------------------------------------------------------

    new_keys = (
        current_keys
        - previous_keys
    )

    # --------------------------------------------------------
    # Removed stocks
    # --------------------------------------------------------

    removed_keys = (
        previous_keys
        - current_keys
    )

    # --------------------------------------------------------
    # Existing stocks
    # --------------------------------------------------------

    existing_keys = (
        current_keys
        & previous_keys
    )

    updated = []

    unchanged = []

    for key in existing_keys:

        old_stock = (
            previous_index[key]
        )

        new_stock = (
            current_index[key]
        )

        # Compare all fields except timestamp.

        old_compare = dict(
            old_stock
        )

        new_compare = dict(
            new_stock
        )

        old_compare.pop(
            "last_updated",
            None
        )

        new_compare.pop(
            "last_updated",
            None
        )

        if old_compare != new_compare:

            updated.append(
                key
            )

        else:

            unchanged.append(
                key
            )

    # --------------------------------------------------------
    # Return change report
    # --------------------------------------------------------

    return {

        "new": sorted(
            new_keys
        ),

        "removed": sorted(
            removed_keys
        ),

        "updated": sorted(
            updated
        ),

        "unchanged": sorted(
            unchanged
        )

    }


# ============================================================
# MARK REMOVED STOCKS INACTIVE
# ============================================================
#
# IMPORTANT:
#
# We do NOT immediately delete securities that disappeared
# from a source.
#
# They are marked inactive.
#
# This protects historical portfolio/chart/transaction data.
#
# ============================================================

def mark_removed_inactive(
    previous,
    removed_keys
):

    result = {}

    for key, stock in previous.items():

        if not isinstance(
            stock,
            dict
        ):

            continue

        updated_stock = dict(
            stock
        )

        if key in removed_keys:

            updated_stock[
                "active"
            ] = False

            updated_stock[
                "status"
            ] = "inactive"

            updated_stock[
                "inactive_reason"
            ] = (
                "Not present in latest "
                "NSE/BSE source"
            )

            updated_stock[
                "inactive_detected_at"
            ] = (
                datetime.utcnow()
                .isoformat()
            )

        result[
            key
        ] = updated_stock

    return result


# ============================================================
# REFRESH MASTER UNIVERSE
# ============================================================

def refresh_master_universe():

    print(
        "============================================================"
    )

    print(
        "GHANIYAA MASTER UNIVERSE REFRESH"
    )

    print(
        "============================================================"
    )

    # ========================================================
    # LOAD PREVIOUS MASTER
    # ========================================================

    previous_master = (
        load_previous_master()
    )

    print(
        f"Previous master count: "
        f"{len(previous_master)}"
    )

    # ========================================================
    # IMPORT CURRENT SOURCES
    # ========================================================

    from backend.services.nse_bse_importer import (
        import_nse_source,
        import_bse_source
    )

    print(
        "Downloading latest NSE universe..."
    )

    nse_stocks = (
        import_nse_source()
    )

    print(
        f"Latest NSE records: "
        f"{len(nse_stocks)}"
    )

    print(
        "Loading latest BSE universe..."
    )

    bse_stocks = (
        import_bse_source()
    )

    print(
        f"Latest BSE records: "
        f"{len(bse_stocks)}"
    )

    # ========================================================
    # SAFETY CHECK
    # ========================================================
    #
    # Never destroy the existing master if both sources fail.
    #
    # ========================================================

    if (
        len(nse_stocks) == 0
        and len(bse_stocks) == 0
    ):

        print(
            "WARNING: Both NSE and BSE "
            "sources returned zero records."
        )

        print(
            "Existing master universe "
            "will NOT be modified."
        )

        return {

            "success": False,

            "reason": (
                "Both exchange sources "
                "returned zero records"
            ),

            "previousCount": len(
                previous_master
            ),

            "currentCount": len(
                previous_master
            ),

            "newStocks": 0,

            "updatedStocks": 0,

            "removedStocks": 0,

            "unchangedStocks": len(
                previous_master
            )

        }

    # ========================================================
    # BUILD NEW MERGED UNIVERSE
    # ========================================================

    from backend.services.stock_universe_merge import (
        merge_nse_bse_universe
    )

    print(
        "Building new NSE + BSE master..."
    )

    merge_result = (
        merge_nse_bse_universe(
            nse_stocks=nse_stocks,
            bse_stocks=bse_stocks
        )
    )

    if not merge_result.get(
        "success",
        False
    ):

        return {

            "success": False,

            "reason": (
                "NSE/BSE merge failed"
            )

        }

    # ========================================================
    # LOAD NEW MASTER
    # ========================================================

    current_master = (
        load_previous_master()
    )

    print(
        f"Current master count: "
        f"{len(current_master)}"
    )

    # ========================================================
    # COMPARE
    # ========================================================

    changes = compare_universes(
        previous_master,
        current_master
    )

    new_keys = changes[
        "new"
    ]

    removed_keys = changes[
        "removed"
    ]

    updated_keys = changes[
        "updated"
    ]

    unchanged_keys = changes[
        "unchanged"
    ]

    # ========================================================
    # HANDLE REMOVED STOCKS
    # ========================================================

    if removed_keys:

        print(
            f"Marking "
            f"{len(removed_keys)} "
            f"removed securities inactive..."
        )

        preserved = (
            mark_removed_inactive(
                previous_master,
                removed_keys
            )
        )

        # Add inactive historical records back into master.

        for key, stock in preserved.items():

            if key not in current_master:

                current_master[
                    key
                ] = stock

    # ========================================================
    # SAVE FINAL MASTER
    # ========================================================

    save_json_file(
        MASTER_UNIVERSE_FILE,
        current_master
    )

    # ========================================================
    # REPORT
    # ========================================================

    report = {

        "success": True,

        "refreshedAt": (
            datetime.utcnow()
            .isoformat()
        ),

        "previousCount": len(
            previous_master
        ),

        "sourceNseCount": len(
            nse_stocks
        ),

        "sourceBseCount": len(
            bse_stocks
        ),

        "currentActiveSourceCount": len(
            current_master
        ),

        "newStocks": len(
            new_keys
        ),

        "updatedStocks": len(
            updated_keys
        ),

        "removedStocks": len(
            removed_keys
        ),

        "unchangedStocks": len(
            unchanged_keys
        ),

        "newStockIdentities": (
            new_keys[:100]
        ),

        "removedStockIdentities": (
            removed_keys[:100]
        ),

        "updatedStockIdentities": (
            updated_keys[:100]
        ),

        "mergeResult": merge_result,

        "masterFile": str(
            MASTER_UNIVERSE_FILE
        )

    }

    # ========================================================
    # SAVE REPORT
    # ========================================================

    save_json_file(
        REFRESH_REPORT_FILE,
        report
    )

    # ========================================================
    # PRINT REPORT
    # ========================================================

    print(
        "============================================================"
    )

    print(
        "MASTER UNIVERSE REFRESH COMPLETE"
    )

    print(
        "============================================================"
    )

    print(
        f"New stocks: "
        f"{len(new_keys)}"
    )

    print(
        f"Updated stocks: "
        f"{len(updated_keys)}"
    )

    print(
        f"Removed stocks: "
        f"{len(removed_keys)}"
    )

    print(
        f"Unchanged stocks: "
        f"{len(unchanged_keys)}"
    )

    print(
        f"Final master count: "
        f"{len(current_master)}"
    )

    print(
        f"Report: "
        f"{REFRESH_REPORT_FILE}"
    )

    return report