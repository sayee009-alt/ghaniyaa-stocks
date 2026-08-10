from backend.stock_registry import (
    get_all_stocks,
    normalize_symbol,
)


def search_stock(query: str):

    query = normalize_symbol(query)

    if not query:
        return []

    stocks = get_all_stocks()

    results = []

    for symbol, info in stocks.items():

        company = info.get(
            "company",
            ""
        )

        sector = info.get(
            "sector",
            "Unknown"
        )

        # ---------------------------------
        # Symbol match
        # ---------------------------------

        if query in symbol.upper():

            results.append({
                "symbol": symbol,
                "company": company,
                "sector": sector
            })

            continue

        # ---------------------------------
        # Company name match
        # ---------------------------------

        if query.lower() in company.lower():

            results.append({
                "symbol": symbol,
                "company": company,
                "sector": sector
            })

            continue

        # ---------------------------------
        # Sector match
        # ---------------------------------

        if query.lower() in sector.lower():

            results.append({
                "symbol": symbol,
                "company": company,
                "sector": sector
            })

    return results