def to_number(value):
    try:
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

        return float(value)

    except (TypeError, ValueError):
        return None


def calculate_score(info):
    score = 50

    pe = to_number(
        info.get("trailingPE")
    )

    roe = to_number(
        info.get("returnOnEquity")
    )

    debt = to_number(
        info.get("debtToEquity")
    )

    if pe is not None and pe < 25:
        score += 15

    if roe is not None and roe > 0.15:
        score += 20

    if debt is not None and debt < 50:
        score += 15

    return min(score, 100)