import yfinance as yf

from backend.stock_registry import get_all_stocks
from backend.services.score import calculate_score
from backend.services.yahoo_symbol_service import get_yahoo_symbol

# ============================================================

# GHANIYAA DYNAMIC STOCK SCREENER

# ============================================================

#
# Supports:
#
# sector
# min_score
# sort
# order
# limit
#
# Example:
#
# /screener
#
# /screener?sector=Technology
#
# /screener?min_score=80
#
# /screener?sort=score
#
# /screener?sort=marketCap&order=desc
#
# /screener?sector=Technology&min_score=80&limit=10
#
# ============================================================

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
    # NORMALIZE FILTERS
    # ========================================================

    if sector:

        sector = sector.strip().lower()


    if min_score is not None:

        try:

            min_score = float(min_score)

        except (TypeError, ValueError):

            min_score = None


    sort = (
        str(sort)
        .strip()
        .lower()
    )


    order = (
        str(order)
        .strip()
        .lower()
    )


    # ========================================================
    # ALLOWED SORT FIELDS
    # ========================================================

    allowed_sort_fields = {

        "score": "score",

        "marketcap": "marketCap",

        "market_cap": "marketCap",

        "price": "price",

        "pe": "pe",

        "roe": "roe",

        "symbol": "symbol",

    }


    # Fallback to score if an invalid sort field is supplied.

    sort_field = allowed_sort_fields.get(
        sort,
        "score"
    )


    # ========================================================
    # PROCESS STOCK UNIVERSE
    # ========================================================

    for registry_key, registry_info in registry.items():

        try:

            # ------------------------------------------------
            # Get actual stock symbol from registry
            # ------------------------------------------------

            symbol = (
                registry_info.get("nse_symbol")
                or registry_info.get("symbol")
                or registry_key
            )

            symbol = (
                str(symbol)
                .strip()
                .upper()
            )


            # ------------------------------------------------
            # Yahoo Finance symbol
            # ------------------------------------------------

            yahoo_symbol = (
                registry_info.get("nse_yahoo_symbol")
                or registry_info.get("bse_yahoo_symbol")
            )

            if not yahoo_symbol:

                yahoo_symbol = get_yahoo_symbol(symbol)


            # ------------------------------------------------
            # Require usable Yahoo symbol
            # ------------------------------------------------

            if not yahoo_symbol:

                invalid.append({

                    "symbol": symbol,

                    "reason": "No Yahoo symbol available"

                })

                continue


            # ------------------------------------------------
            # Yahoo Finance
            # ------------------------------------------------

            ticker = yf.Ticker(yahoo_symbol)

            info = ticker.info


            # ------------------------------------------------
            # Company
            # ------------------------------------------------

            company = info.get(
                "longName"
            )

            if not company:

                company = registry_info.get(
                    "company"
                )


            # ------------------------------------------------
            # Current price
            # ------------------------------------------------

            current_price = info.get(
                "currentPrice"
            )


            # ------------------------------------------------
            # Market cap
            # ------------------------------------------------

            market_cap = info.get(
                "marketCap"
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
                    )

                })

                continue


            # ------------------------------------------------
            # Sector
            # ------------------------------------------------

            stock_sector = info.get(
                "sector"
            )

            if not stock_sector:

                stock_sector = registry_info.get(
                    "sector",
                    "Unknown"
                )


            # ------------------------------------------------
            # Calculate Ghaniyaa Score
            # ------------------------------------------------

            score = calculate_score(
                info
            )


            # =================================================
            # SECTOR FILTER
            # =================================================

            if sector:

                if sector not in stock_sector.lower():

                    continue


            # =================================================
            # SCORE FILTER
            # =================================================

            if min_score is not None:

                if score is None:

                    continue

                if score < min_score:

                    continue


            # =================================================
            # ADD VALID STOCK
            # =================================================

            valid_stocks.append({

                "symbol": symbol,

                "company": (
                    company
                    or "Unknown"
                ),

                "price": current_price,

                "sector": stock_sector,

                "marketCap": market_cap,

                "pe": info.get(
                    "trailingPE"
                ),

                "roe": info.get(
                    "returnOnEquity"
                ),

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
                )

            })

            continue


    # ========================================================
    # SORT
    # ========================================================

    def sort_value(stock):

        value = stock.get(
            sort_field
        )

        # ----------------------------------------------------
        # Missing numeric values go to the bottom.
        # ----------------------------------------------------

        if value is None:

            if sort_field == "symbol":

                return ""

            return float("-inf")


        return value


    reverse = (
        order != "asc"
    )


    valid_stocks.sort(
        key=sort_value,
        reverse=reverse
    )


    # ========================================================
    # ASSIGN RANK AFTER FILTERING + SORTING
    # ========================================================

    for index, stock in enumerate(
        valid_stocks,
        start=1
    ):

        stock["rank"] = index


    # ========================================================
    # APPLY LIMIT
    # ========================================================

    if limit is not None:

        try:

            limit = int(limit)

            if limit > 0:

                valid_stocks = (
                    valid_stocks[:limit]
                )

        except (TypeError, ValueError):

            pass


    # ========================================================
    # SORT INVALID STOCKS
    # ========================================================

    invalid.sort(
        key=lambda stock: stock["symbol"]
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

        }

    }