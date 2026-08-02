def calculate_score(info):
    score = 50

    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity")
    debt = info.get("debtToEquity")

    if pe and pe < 25:
        score += 15

    if roe and roe > 0.15:
        score += 20

    if debt and debt < 50:
        score += 15

    return min(score, 100)