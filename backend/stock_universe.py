import json
from pathlib import Path


# ============================================================
# GHANIYAA MASTER STOCK UNIVERSE
# ============================================================
#
# IMPORTANT:
#
# The authoritative universe is now:
#
#     database/master_stock_universe.json
#
# This module exists as a compatibility layer for existing
# Ghaniyaa code that imports:
#
#     from backend.stock_universe import STOCK_UNIVERSE
#
# It must NEVER maintain a separate hard-coded stock list.
#
# ============================================================


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(
    __file__
).resolve().parents[1]


# ============================================================
# MASTER UNIVERSE FILE
# ============================================================

MASTER_UNIVERSE_FILE = (
    BASE_DIR
    / "database"
    / "master_stock_universe.json"
)


# ============================================================
# LOAD MASTER UNIVERSE
# ============================================================

def _load_master_universe():

    if not MASTER_UNIVERSE_FILE.exists():

        print(
            "ERROR: Master stock universe file not found:"
        )

        print(
            MASTER_UNIVERSE_FILE
        )

        return {}

    try:

        with open(
            MASTER_UNIVERSE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        print(
            "ERROR: Invalid master stock universe JSON:"
        )

        print(error)

        return {}

    except OSError as error:

        print(
            "ERROR: Unable to read master stock universe:"
        )

        print(error)

        return {}

    if not isinstance(data, dict):

        print(
            "ERROR: master_stock_universe.json "
            "must contain a dictionary."
        )

        return {}

    return data


# ============================================================
# AUTHORITATIVE STOCK UNIVERSE
# ============================================================

STOCK_UNIVERSE = _load_master_universe()


# ============================================================
# METADATA
# ============================================================

STOCK_UNIVERSE_FILE = str(
    MASTER_UNIVERSE_FILE
)

STOCK_UNIVERSE_COUNT = len(
    STOCK_UNIVERSE
)


# ============================================================
# STARTUP VALIDATION
# ============================================================

if STOCK_UNIVERSE_COUNT == 0:

    print(
        "WARNING: Ghaniyaa STOCK_UNIVERSE is empty."
    )

else:

    print(
        "Ghaniyaa STOCK_UNIVERSE loaded: "
        f"{STOCK_UNIVERSE_COUNT} records"
    )