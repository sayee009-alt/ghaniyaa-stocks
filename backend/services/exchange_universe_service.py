"""
Ghaniyaa Stocks
Exchange Universe Service

Downloads official exchange security-master data from:
    - NSE India
    - BSE India

This service is responsible ONLY for obtaining raw exchange data.

Normalization, merging, deduplication and persistence are handled
by stock_universe_service.py.
"""

from __future__ import annotations

import io
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

EXCHANGE_DATA_DIR = (
    BASE_DIR
    / "database"
    / "exchange_universe"
)

EXCHANGE_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# NSE
# ============================================================

NSE_EQUITY_URL = (
    "https://nsearchives.nseindia.com/"
    "content/equities/EQUITY_L.csv"
)


# ============================================================
# BSE
# ============================================================

BSE_SCRIP_MASTER_URL = (
    "https://api.bseindia.com/"
    "BseIndiaAPI/api/ListofScripData/w"
)


# ============================================================
# HTTP SESSION
# ============================================================

def create_session():
    """
    Create a browser-like HTTP session.

    Exchange websites may reject requests that look like
    automated clients, so we provide normal request headers.
    """

    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    })

    return session


# ============================================================
# TIMESTAMP
# ============================================================

def utc_timestamp():
    """
    Return a filesystem-safe UTC timestamp.
    """

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S"
    )


# ============================================================
# NSE DOWNLOAD
# ============================================================

def download_nse_equity_master(
    timeout: int = 30,
    retries: int = 3,
):
    """
    Download NSE equity security master.

    Returns:
        pandas.DataFrame

    Raises:
        RuntimeError
    """

    session = create_session()

    last_error = None

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            response = session.get(
                NSE_EQUITY_URL,
                timeout=timeout
            )

            response.raise_for_status()

            content = response.content

            if not content:
                raise RuntimeError(
                    "NSE returned an empty response."
                )

            df = pd.read_csv(
                io.BytesIO(content)
            )

            if df.empty:
                raise RuntimeError(
                    "NSE equity master is empty."
                )

            # ------------------------------------------------
            # Save raw source
            # ------------------------------------------------

            filename = (
                "nse_equity_"
                f"{utc_timestamp()}.csv"
            )

            output_file = (
                EXCHANGE_DATA_DIR
                / filename
            )

            output_file.write_bytes(
                content
            )

            return df

        except Exception as error:

            last_error = error

            print(
                f"NSE download attempt "
                f"{attempt}/{retries} failed: "
                f"{error}"
            )

            if attempt < retries:

                time.sleep(
                    2 * attempt
                )

    raise RuntimeError(
        "Unable to download NSE equity master."
        f" Last error: {last_error}"
    )


# ============================================================
# BSE DOWNLOAD
# ============================================================

def download_bse_scrip_master(
    timeout: int = 30,
    retries: int = 3,
):
    """
    Download BSE scrip master.

    BSE's API response format can change, so this function
    deliberately returns the raw decoded response.

    Returns:
        dict/list depending on BSE response.

    Raises:
        RuntimeError
    """

    session = create_session()

    last_error = None

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            response = session.get(
                BSE_SCRIP_MASTER_URL,
                timeout=timeout
            )

            response.raise_for_status()

            if not response.content:
                raise RuntimeError(
                    "BSE returned an empty response."
                )

            content = response.content

            # ------------------------------------------------
            # Save raw response
            # ------------------------------------------------

            filename = (
                "bse_scrip_master_"
                f"{utc_timestamp()}.json"
            )

            output_file = (
                EXCHANGE_DATA_DIR
                / filename
            )

            output_file.write_bytes(
                content
            )

            try:

                return response.json()

            except ValueError:

                return {
                    "raw_text": response.text
                }

        except Exception as error:

            last_error = error

            print(
                f"BSE download attempt "
                f"{attempt}/{retries} failed: "
                f"{error}"
            )

            if attempt < retries:

                time.sleep(
                    2 * attempt
                )

    raise RuntimeError(
        "Unable to download BSE scrip master."
        f" Last error: {last_error}"
    )


# ============================================================
# NSE COLUMN INSPECTION
# ============================================================

def get_nse_columns():
    """
    Download NSE master and return its column names.

    Useful while the exchange format evolves.
    """

    df = download_nse_equity_master()

    return list(
        df.columns
    )


# ============================================================
# BSE RESPONSE INSPECTION
# ============================================================

def get_bse_raw():
    """
    Download and return the raw BSE response.
    """

    return download_bse_scrip_master()


# ============================================================
# SOURCE STATUS
# ============================================================

def get_exchange_source_status():
    """
    Return information about configured exchange sources.
    """

    return {
        "nse": {
            "name": "NSE India",
            "source": NSE_EQUITY_URL,
            "configured": True,
        },

        "bse": {
            "name": "BSE India",
            "source": BSE_SCRIP_MASTER_URL,
            "configured": True,
        },
    }


# ============================================================
# DOWNLOAD BOTH
# ============================================================

def download_exchange_universe():
    """
    Download both NSE and BSE raw universe sources.

    This function does NOT merge or normalize them.

    Returns:
        {
            "nse": DataFrame,
            "bse": raw response
        }
    """

    nse = download_nse_equity_master()

    bse = download_bse_scrip_master()

    return {
        "nse": nse,
        "bse": bse,
    }


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Ghaniyaa Exchange Universe Service"
    )

    print(
        "\nConfigured sources:"
    )

    print(
        get_exchange_source_status()
    )

    print(
        "\nDownloading NSE..."
    )

    try:

        nse = (
            download_nse_equity_master()
        )

        print(
            f"NSE rows: {len(nse)}"
        )

        print(
            "NSE columns:"
        )

        print(
            list(nse.columns)
        )

    except Exception as error:

        print(
            f"NSE failed: {error}"
        )

    print(
        "\nDownloading BSE..."
    )

    try:

        bse = (
            download_bse_scrip_master()
        )

        if isinstance(bse, dict):

            print(
                "BSE response keys:"
            )

            print(
                list(bse.keys())[:20]
            )

        elif isinstance(bse, list):

            print(
                f"BSE rows: {len(bse)}"
            )

        else:

            print(
                type(bse)
            )

    except Exception as error:

        print(
            f"BSE failed: {error}"
        )