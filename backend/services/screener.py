import yfinance as yf

from backend.stock_registry import get_all_stocks
from backend.services.score import calculate_score
from backend.services.yahoo_symbol_service import get_yahoo_symbol


# ============================================================
# GHANIYAA STOCK SCREENER
# ============================================================
#
# Supports:
#
#   sector
#   min_score
#   sort
#   order
#   limit
#
# Examples:
#
#   /screener?limit=5
#   /screener?sector=Technology&limit=5
#   /screener?min_score=80&limit=10
#   /screener?sort=marketCap&order=desc&limit=10
#
# IMPORTANT:
#
# limit is applied DURING processing.
# This prevents a test such as limit=5 from processing
# the entire 8,018-stock universe.
#
# ============================================================


def _safe_float(value):
    """
    Convert a value to float when possible.

    Yahoo Finance sometimes returns strings, None,
    NaN, or other unexpected values.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        value = float(value)

        # Reject NaN / infinity
        if value != value:
            return None

        if value == float("inf"):
            return None

        if value == float("-inf"):
            return None

        return value

    except (TypeError, ValueError):
        return None


def _safe_number(value):
    """
    Preserve integer-looking values while making sure
    strings cannot break sorting/comparisons.
    """

    number = _safe_float(value)

    if number is None:
        return None

    return number


def _safe_score(info):
    """
    Calculate Ghaniyaa score safely.

    calculate_score() is the existing scoring engine,
    but Yahoo values can occasionally have unexpected
    types. Normalize the relevant values first.
    """

    safe_info = dict(info)

    safe_info["trailingPE"] = _safe_number(
        info.get("trailingPE")
    )

    safe_info["returnOnEquity"] = _safe_number(
        info.get("returnOnEquity")
    )

    safe_info["debtToEquity"] = _safe_number(
        info.get("debtToEquity")
    )

    try:
        score = calculate_score(safe_info)

        return _safe_number(score)

    except Exception:
        return None


def _safe_sort_value(stock, sort_field):
    """
    Return a consistent value for sorting.

    Missing numeric values are placed at the bottom.
    Strings are never compared against numbers.
    """

    value = stock.get(sort_field)

    if sort_field == "symbol":
        return str(value or "").upper()

    number = _safe_float(value)

    if number is None:
        return float("-inf")

    return number


def screen_all_stocks(
    sector=None,
    min_score=None,
    sort="score",
    order="desc",
    limit=None,
):

    valid_stocks = []
    invalid = []

    registry = get_all_stocks()

    # ========================================================
    # NORMALIZE LIMIT
    # ========================================================

    if limit is not None:

        try:
            limit = int(limit)

        except (TypeError, ValueError):

            limit = None

        if limit is not None and limit <= 0:
            limit = None

    # ========================================================
    # NORMALIZE SECTOR
    # ========================================================

    if sector:

        sector = str(
            sector
        ).strip().lower()

        if not sector:
            sector = None

    # ========================================================
    # NORMALIZE MIN SCORE
    # ========================================================

    if min_score is not None:

        min_score = _safe_float(
            min_score
        )

    # ========================================================
    # NORMALIZE SORT
    # ========================================================

    sort = (
        str(sort)
        .strip()
        .lower()
    )

    allowed_sort_fields = {

        "score": "score",

        "marketcap": "marketCap",

        "market_cap": "marketCap",

        "price": "price",

        "pe": "pe",

        "roe": "roe",

        "symbol": "symbol",

    }

    sort_field = allowed_sort_fields.get(
        sort,
        "score"
    )

    # ========================================================
    # NORMALIZE ORDER
    # ========================================================

    order = (
        str(order)
        .strip()
        .lower()
    )

    reverse = (
        order != "asc"
    )

    # ========================================================
    # PROCESS STOCK UNIVERSE
    # ========================================================

    processed = 0

    for registry_key, registry_info in registry.items():

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # If limit is supplied, stop processing once we have
        # enough VALID stocks.
        #
        # This makes limit=5 a genuinely small test.
        # ----------------------------------------------------

        if (
            limit is not None
            and len(valid_stocks) >= limit
        ):

            break

        processed += 1

        symbol = str(
            registry_key
        ).strip().upper()

        try:

            # ------------------------------------------------
            # Registry information
            # ------------------------------------------------

            if not isinstance(
                registry_info,
                dict
            ):

                registry_info = {}

            symbol = str(
                registry_info.get(
                    "nse_symbol"
                )
                or registry_info.get(
                    "symbol"
                )
                or registry_key
            ).strip().upper()

            # ------------------------------------------------
            # Yahoo symbol
            # ------------------------------------------------

            yahoo_symbol = (
                registry_info.get(
                    "nse_yahoo_symbol"
                )
                or registry_info.get(
                    "bse_yahoo_symbol"
                )
            )

            if not yahoo_symbol:

                yahoo_symbol = get_yahoo_symbol(
                    symbol
                )

            if not yahoo_symbol:

                invalid.append({

                    "symbol": symbol,

                    "reason": (
                        "No Yahoo symbol available"
                    ),

                })

                continue

            # ------------------------------------------------
            # Yahoo Finance
            # ------------------------------------------------

            ticker = yf.Ticker(
                yahoo_symbol
            )

            # ------------------------------------------------
            # ticker.info can sometimes hang/fail.
            #
            # Keep this isolated inside the stock-level
            # exception so one stock cannot terminate the
            # entire screener.
            # ------------------------------------------------

            info = ticker.info

            if not isinstance(
                info,
                dict
            ):

                info = {}

            # ------------------------------------------------
            # Company
            # ------------------------------------------------

            company = (
                info.get(
                    "longName"
                )
                or info.get(
                    "shortName"
                )
                or registry_info.get(
                    "company"
                )
                or "Unknown"
            )

            # ------------------------------------------------
            # Current price
            # ------------------------------------------------

            current_price = _safe_float(
                info.get(
                    "currentPrice"
                )
            )

            # ------------------------------------------------
            # Fallback price
            #
            # Some Yahoo responses don't provide currentPrice.
            # Try regularMarketPrice.
            # ------------------------------------------------

            if current_price is None:

                current_price = _safe_float(
                    info.get(
                        "regularMarketPrice"
                    )
                )

            # ------------------------------------------------
            # Price is required
            # ------------------------------------------------

            if current_price is None:

                invalid.append({

                    "symbol": symbol,

                    "reason": (
                        "Current market price "
                        "is unavailable"
                    ),

                })

                continue

            # ------------------------------------------------
            # Market cap
            # ------------------------------------------------

            market_cap = _safe_float(
                info.get(
                    "marketCap"
                )
            )

            # ------------------------------------------------
            # Sector
            # ------------------------------------------------

            stock_sector = (
                info.get(
                    "sector"
                )
                or registry_info.get(
                    "sector"
                )
                or "Unknown"
            )

            stock_sector = str(
                stock_sector
            )

            # ------------------------------------------------
            # Sector filter
            #
            # Apply BEFORE calculating the score.
            # ------------------------------------------------

            if sector:

                if sector not in (
                    stock_sector.lower()
                ):

                    continue

            # ------------------------------------------------
            # PE
            # ------------------------------------------------

            pe = _safe_float(
                info.get(
                    "trailingPE"
                )
            )

            # ------------------------------------------------
            # ROE
            # ------------------------------------------------

            roe = _safe_float(
                info.get(
                    "returnOnEquity"
                )
            )

            # ------------------------------------------------
            # Ghaniyaa Score
            # ------------------------------------------------

            score = _safe_score(
                info
            )

            # ------------------------------------------------
            # Score filter
            # ------------------------------------------------

            if min_score is not None:

                if score is None:
                    continue

                if score < min_score:
                    continue

            # ------------------------------------------------
            # Add valid stock
            # ------------------------------------------------

            valid_stocks.append({

                "symbol": symbol,

                "company": company,

                "price": current_price,

                "sector": stock_sector,

                "marketCap": market_cap,

                "pe": pe,

                "roe": roe,

                "score": score,

            })

        except Exception as e:

            # ------------------------------------------------
            # One stock must never stop the screener.
            # ------------------------------------------------

            print(
                f"Screener error for "
                f"{symbol}: {e}"
            )

            invalid.append({

                "symbol": symbol,

                "reason": (
                    "Market data request failed"
                ),

            })

            continue

    # ========================================================
    # SORT VALID STOCKS
    # ========================================================

    valid_stocks.sort(
        key=lambda stock: _safe_sort_value(
            stock,
            sort_field
        ),
        reverse=reverse
    )

    # ========================================================
    # APPLY RANK AFTER SORTING
    # ========================================================

    for index, stock in enumerate(
        valid_stocks,
        start=1
    ):

        stock["rank"] = index

    # ========================================================
    # APPLY FINAL LIMIT
    #
    # This is also kept here as protection.
    # ========================================================

    if limit is not None:

        valid_stocks = (
            valid_stocks[:limit]
        )

    # ========================================================
    # SORT INVALID STOCKS
    # ========================================================

    invalid.sort(
        key=lambda stock: str(
            stock.get(
                "symbol",
                ""
            )
        )
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "stocks": valid_stocks,

        "count": len(valid_stocks),

        "invalidCount": len(invalid),

        "invalid": invalid,

        "filters": {

            "sector": sector,

            "minScore": min_score,

            "sort": sort_field,

            "order": (
                "asc"
                if order == "asc"
                else "desc"
            ),

            "limit": limit,

        },

        "processed": processed,

    }