import csv
import io
import json
import requests
from datetime import datetime


# ============================================================
# GHANIYAA NSE + BSE SOURCE IMPORTER
# ============================================================

NSE_EQUITY_URL = (
    "https://nsearchives.nseindia.com/"
    "content/equities/EQUITY_L.csv"
)

BSE_SOURCE_URL = (
    "https://api.bseindia.com/"
    "BseIndiaAPI/api/ListofScripData/w"
)


# ============================================================
# COMMON HEADERS
# ============================================================

NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    ),
    "Accept": (
        "text/csv,application/csv,"
        "application/octet-stream,text/plain,*/*"
    ),
    "Referer": "https://www.nseindia.com/",
}


BSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    ),
    "Accept": (
        "application/json, text/plain, */*"
    ),
    "Referer": "https://www.bseindia.com/",
    "Origin": "https://www.bseindia.com",
}


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
# NSE IMPORTER
# ============================================================

def import_nse_source():

    print("Downloading NSE...")

    try:

        response = requests.get(
            NSE_EQUITY_URL,
            headers=NSE_HEADERS,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as error:

        print(
            f"NSE download failed: {error}"
        )

        return []

    try:

        text = response.content.decode(
            "utf-8-sig"
        )

    except UnicodeDecodeError:

        try:

            text = response.content.decode(
                "latin-1"
            )

        except Exception as error:

            print(
                f"NSE decode failed: {error}"
            )

            return []

    try:

        reader = csv.DictReader(
            io.StringIO(text)
        )

        rows = list(reader)

    except Exception as error:

        print(
            f"NSE CSV parsing failed: {error}"
        )

        return []

    print(
        f"NSE rows: {len(rows)}"
    )

    if not rows:

        print(
            "NSE returned no rows."
        )

        return []

    print(
        "NSE columns:"
    )

    print(
        list(rows[0].keys())
    )

    normalized = []

    failed = 0

    for row in rows:

        try:

            symbol = (
                row.get("SYMBOL")
                or row.get("Symbol")
                or row.get("symbol")
            )

            company = (
                row.get("NAME OF COMPANY")
                or row.get("NAME_OF_COMPANY")
                or row.get("Name of Company")
                or row.get("Company Name")
            )

            series = (
                row.get(" SERIES")
                or row.get("SERIES")
                or row.get(" Series")
                or ""
            )

            listing_date = (
                row.get(" DATE OF LISTING")
                or row.get("DATE OF LISTING")
                or row.get("Date of Listing")
                or ""
            )

            isin = (
                row.get(" ISIN NUMBER")
                or row.get("ISIN NUMBER")
                or row.get("ISIN")
                or ""
            )

            paid_up_value = (
                row.get(" PAID UP VALUE")
                or row.get("PAID UP VALUE")
                or ""
            )

            market_lot = (
                row.get(" MARKET LOT")
                or row.get("MARKET LOT")
                or ""
            )

            face_value = (
                row.get(" FACE VALUE")
                or row.get("FACE VALUE")
                or ""
            )

            symbol = normalize_symbol(
                symbol
            )

            if not symbol:

                failed += 1

                continue

            series = str(
                series
            ).strip().upper()

            company = (
                str(company).strip()
                if company
                else symbol
            )

            isin = (
                str(isin).strip()
                if isin
                else None
            )

            listing_date = (
                str(listing_date).strip()
                if listing_date
                else None
            )

            normalized.append({

                "symbol": symbol,

                "company": company,

                "isin": isin,

                "series": series,

                "listing_date": listing_date,

                "paid_up_value": (
                    paid_up_value
                    if paid_up_value
                    else None
                ),

                "market_lot": (
                    market_lot
                    if market_lot
                    else None
                ),

                "face_value": (
                    face_value
                    if face_value
                    else None
                ),

                "exchange": "NSE",

                "exchanges": [
                    "NSE"
                ],

                "yahoo_symbol": (
                    f"{symbol}.NS"
                ),

                "active": True,

                "status": "active",

                "source": "NSE India",

                "source_url": NSE_EQUITY_URL,

                "last_updated": (
                    datetime.utcnow()
                    .isoformat()
                )

            })

        except Exception as error:

            failed += 1

            print(
                f"NSE row normalization failed: "
                f"{error}"
            )

    print(
        f"NSE normalized rows: "
        f"{len(normalized)}"
    )

    print(
        f"NSE failed rows: "
        f"{failed}"
    )

    if normalized:

        print(
            "NSE sample:"
        )

        print(
            normalized[0]
        )

    return normalized


# ============================================================
# GHANIYAA BSE EQUITY MASTER IMPORTER
# ============================================================
#
# Source:
# BSE Equity.csv
#
# Expected columns:
#
#   Security Code
#   Issuer Name
#   Security Id
#   Security Name
#   Status
#   Group
#   Face Value
#   ISIN No
#   Instrument
#
# This function reads a local BSE Equity master CSV and
# converts it into Ghaniyaa's normalized stock format.
#
# IMPORTANT:
#
# This function does NOT modify master_stock_universe.json.
# The merge/import service will do that separately.
#
# ============================================================

def import_bse_source(
    csv_path=None
):

    import csv
    from pathlib import Path
    from datetime import datetime

    print(
        "Loading BSE Equity master..."
    )

    # ========================================================
    # DEFAULT FILE LOCATION
    # ========================================================

    if csv_path is None:

        base_dir = Path(
            __file__
        ).resolve().parents[2]

        csv_path = (
            base_dir
            / "database"
            / "Equity.csv"
        )

    else:

        csv_path = Path(
            csv_path
        )

    # ========================================================
    # CHECK FILE
    # ========================================================

    if not csv_path.exists():

        print(
            "BSE Equity master file not found:"
        )

        print(
            csv_path
        )

        return []

    print(
        f"BSE source file: {csv_path}"
    )

    # ========================================================
    # READ CSV
    # ========================================================

    try:

        with open(
            csv_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(
                file
            )

            rows = list(
                reader
            )

    except UnicodeDecodeError:

        try:

            with open(
                csv_path,
                "r",
                encoding="latin-1",
                newline=""
            ) as file:

                reader = csv.DictReader(
                    file
                )

                rows = list(
                    reader
                )

        except Exception as error:

            print(
                f"BSE CSV read failed: {error}"
            )

            return []

    except Exception as error:

        print(
            f"BSE CSV read failed: {error}"
        )

        return []

    # ========================================================
    # BASIC VALIDATION
    # ========================================================

    print(
        f"BSE rows: {len(rows)}"
    )

    if not rows:

        print(
            "BSE file contains no rows."
        )

        return []

    print(
        "BSE columns:"
    )

    print(
        list(rows[0].keys())
    )

    # ========================================================
    # EXPECTED COLUMNS
    # ========================================================

    required_columns = {

        "Security Code",

        "Issuer Name",

        "Security Id",

        "Security Name",

        "Status",

        "Group",

        "Face Value",

        "ISIN No",

        "Instrument",

    }

    actual_columns = set(
        rows[0].keys()
    )

    missing_columns = (
        required_columns
        - actual_columns
    )

    if missing_columns:

        print(
            "BSE file is missing "
            "expected columns:"
        )

        print(
            sorted(
                missing_columns
            )
        )

        return []

    # ========================================================
    # NORMALIZED RESULT
    # ========================================================

    normalized = []

    failed = 0

    skipped_non_equity = 0

    skipped_invalid = 0

    # ========================================================
    # PROCESS ROWS
    # ========================================================

    for row in rows:

        try:

            # ------------------------------------------------
            # SECURITY CODE
            # ------------------------------------------------

            security_code = (
                row.get(
                    "Security Code"
                )
            )

            if security_code is None:

                skipped_invalid += 1

                continue

            security_code = (
                str(
                    security_code
                )
                .strip()
            )

            if not security_code:

                skipped_invalid += 1

                continue

            # ------------------------------------------------
            # REMOVE .0 FROM NUMERIC CSV VALUES
            # ------------------------------------------------

            if security_code.endswith(
                ".0"
            ):

                security_code = (
                    security_code[:-2]
                )

            # ------------------------------------------------
            # ISSUER
            # ------------------------------------------------

            company = (
                row.get(
                    "Issuer Name"
                )
                or row.get(
                    "Security Name"
                )
                or "Unknown"
            )

            company = (
                str(company)
                .strip()
            )

            # ------------------------------------------------
            # BSE SECURITY ID
            # ------------------------------------------------

            security_id = (
                row.get(
                    "Security Id"
                )
            )

            security_id = (

                str(
                    security_id
                )
                .strip()

                if security_id

                else None
            )

            # ------------------------------------------------
            # SECURITY NAME
            # ------------------------------------------------

            security_name = (
                row.get(
                    "Security Name"
                )
            )

            security_name = (

                str(
                    security_name
                )
                .strip()

                if security_name

                else None
            )

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            status = (
                row.get(
                    "Status"
                )
                or ""
            )

            status = (
                str(status)
                .strip()
            )

            status_lower = (
                status
                .lower()
            )

            active = (
                status_lower
                == "active"
            )

            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------

            group = (
                row.get(
                    "Group"
                )
                or ""
            )

            group = (
                str(group)
                .strip()
            )

            # ------------------------------------------------
            # FACE VALUE
            # ------------------------------------------------

            face_value = (
                row.get(
                    "Face Value"
                )
            )

            face_value = (

                str(
                    face_value
                )
                .strip()

                if face_value

                else None
            )

            # ------------------------------------------------
            # ISIN
            # ------------------------------------------------

            isin = (
                row.get(
                    "ISIN No"
                )
            )

            isin = (

                str(
                    isin
                )
                .strip()
                .upper()

                if isin

                else None
            )

            # ------------------------------------------------
            # INSTRUMENT
            # ------------------------------------------------

            instrument = (
                row.get(
                    "Instrument"
                )
                or ""
            )

            instrument = (
                str(instrument)
                .strip()
            )

            # ------------------------------------------------
            # EQUITY FILTER
            # ------------------------------------------------

            if instrument:

                if (
                    instrument
                    .strip()
                    .lower()
                    != "equity"
                ):

                    skipped_non_equity += 1

                    continue

            # ------------------------------------------------
            # NORMALIZED BSE RECORD
            # ------------------------------------------------

            stock = {

                # --------------------------------------------
                # BSE IDENTIFIERS
                # --------------------------------------------

                "bse_scrip_code": (
                    security_code
                ),

                "symbol": (
                    security_id
                    or security_code
                ),

                "scrip_id": (
                    security_id
                ),

                # --------------------------------------------
                # COMPANY
                # --------------------------------------------

                "company": (
                    company
                    or "Unknown"
                ),

                "security_name": (
                    security_name
                ),

                # --------------------------------------------
                # MARKET INFORMATION
                # --------------------------------------------

                "isin": (
                    isin
                ),

                "status": (
                    "active"
                    if active
                    else "inactive"
                ),

                "active": (
                    active
                ),

                "group": (
                    group
                    or None
                ),

                "face_value": (
                    face_value
                ),

                "instrument": (
                    instrument
                    or "Equity"
                ),

                # --------------------------------------------
                # EXCHANGE
                # --------------------------------------------

                "exchange": "BSE",

                "exchanges": [
                    "BSE"
                ],

                # --------------------------------------------
                # YAHOO
                # --------------------------------------------
                #
                # BSE symbols generally require .BO.
                #
                # Example:
                #
                # RELIANCE.BO
                #
                # --------------------------------------------

                "yahoo_symbol": (
                    f"{security_id}.BO"
                    if security_id
                    else None
                ),

                # --------------------------------------------
                # SOURCE
                # --------------------------------------------

                "source": (
                    "BSE India"
                ),

                "source_url": (
                    str(
                        csv_path
                    )
                ),

                # --------------------------------------------
                # TIMESTAMP
                # --------------------------------------------

                "last_updated": (
                    datetime.utcnow()
                    .isoformat()
                ),

            }

            normalized.append(
                stock
            )

        except Exception as error:

            failed += 1

            print(
                "BSE row normalization failed:"
            )

            print(
                error
            )

            continue

    # ========================================================
    # RESULT
    # ========================================================

    print(
        f"BSE normalized rows: "
        f"{len(normalized)}"
    )

    print(
        f"BSE skipped non-equity rows: "
        f"{skipped_non_equity}"
    )

    print(
        f"BSE skipped invalid rows: "
        f"{skipped_invalid}"
    )

    print(
        f"BSE failed rows: "
        f"{failed}"
    )

    # ========================================================
    # SAMPLE
    # ========================================================

    if normalized:

        print(
            "BSE sample:"
        )

        print(
            normalized[0]
        )

    return normalized