from fastapi import APIRouter
import yfinance as yf

router = APIRouter()


@router.get("/thesis/{symbol}")
def get_thesis(symbol: str):

    symbol = symbol.upper()

    stock = yf.Ticker(symbol + ".NS")

    info = stock.info

    history = stock.history(period="6mo")

    if history.empty:
        return {
            "error": "No market data found",
            "symbol": symbol
        }

    close = history["Close"].dropna()

    if close.empty:
        return {
            "error": "No price data available",
            "symbol": symbol
        }

    current_price = float(close.iloc[-1])

    # -----------------------------
    # MOVING AVERAGES
    # -----------------------------

    ma20 = float(
        close.rolling(20).mean().iloc[-1]
    )

    ma50 = float(
        close.rolling(50).mean().iloc[-1]
    )

    # -----------------------------
    # MOMENTUM
    # -----------------------------

    if len(close) >= 21:

        momentum = (
            (current_price / float(close.iloc[-21])) - 1
        ) * 100

    else:

        momentum = 0

    # -----------------------------
    # RSI
    # -----------------------------

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    rsi_value = float(rsi.iloc[-1])

    if rsi_value != rsi_value:
        rsi_value = 50

    # -----------------------------
    # FUNDAMENTAL DATA
    # -----------------------------

    pe = info.get("trailingPE")

    roe = info.get("returnOnEquity")

    debt_to_equity = info.get("debtToEquity")

    revenue_growth = info.get(
        "revenueGrowth"
    )

    profit_margin = info.get(
        "profitMargins"
    )

    # -----------------------------
    # SCORE
    # -----------------------------

    fundamental_score = 50

    if pe is not None:

        if pe < 25:
            fundamental_score += 10

        elif pe > 50:
            fundamental_score -= 10

    if roe is not None:

        if roe > 0.15:
            fundamental_score += 15

        elif roe < 0.05:
            fundamental_score -= 10

    if debt_to_equity is not None:

        if debt_to_equity < 100:
            fundamental_score += 10

        elif debt_to_equity > 200:
            fundamental_score -= 10

    if revenue_growth is not None:

        if revenue_growth > 0.10:
            fundamental_score += 10

        elif revenue_growth < 0:
            fundamental_score -= 10

    fundamental_score = max(
        0,
        min(100, fundamental_score)
    )

    # -----------------------------
    # TECHNICAL SCORE
    # -----------------------------

    technical_score = 50

    if current_price > ma20:
        technical_score += 10
    else:
        technical_score -= 10

    if ma20 > ma50:
        technical_score += 15
    else:
        technical_score -= 15

    if momentum > 5:
        technical_score += 10

    elif momentum < -5:
        technical_score -= 10

    if rsi_value < 30:
        technical_score += 5

    elif rsi_value > 70:
        technical_score -= 5

    technical_score = max(
        0,
        min(100, technical_score)
    )

    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = round(
        fundamental_score * 0.60
        +
        technical_score * 0.40
    )

    # -----------------------------
    # RECOMMENDATION
    # -----------------------------

    if final_score >= 70:

        recommendation = "BUY"

    elif final_score >= 50:

        recommendation = "HOLD"

    else:

        recommendation = "SELL"

    # -----------------------------
    # POSITIVE FACTORS
    # -----------------------------

    positives = []

    if fundamental_score >= 70:
        positives.append(
            "Strong fundamental quality"
        )

    if current_price > ma20:
        positives.append(
            "Price is above the 20-day moving average"
        )

    if ma20 > ma50:
        positives.append(
            "20-day moving average is above 50-day moving average"
        )

    if momentum > 5:
        positives.append(
            "Positive 20-day momentum"
        )

    if roe is not None and roe > 0.15:
        positives.append(
            "Strong return on equity"
        )

    if revenue_growth is not None and revenue_growth > 0.10:
        positives.append(
            "Healthy revenue growth"
        )

    if debt_to_equity is not None and debt_to_equity < 100:
        positives.append(
            "Debt level appears manageable"
        )

    # -----------------------------
    # RISKS
    # -----------------------------

    risks = []

    if pe is not None and pe > 40:
        risks.append(
            "Valuation appears relatively high"
        )

    if rsi_value > 70:
        risks.append(
            "RSI indicates potentially overbought conditions"
        )

    if momentum < -5:
        risks.append(
            "Negative recent momentum"
        )

    if debt_to_equity is not None and debt_to_equity > 200:
        risks.append(
            "High debt-to-equity ratio"
        )

    if revenue_growth is not None and revenue_growth < 0:
        risks.append(
            "Revenue growth is currently negative"
        )

    if not risks:
        risks.append(
            "Continue monitoring market volatility"
        )

    # -----------------------------
    # OVERALL VIEW
    # -----------------------------

    if final_score >= 70:

        overall_view = "Positive"

    elif final_score >= 50:

        overall_view = "Neutral"

    else:

        overall_view = "Negative"

    return {

        "symbol": symbol,

        "currentPrice": round(
            current_price,
            2
        ),

        "fundamentalScore": fundamental_score,

        "technicalScore": technical_score,

        "finalScore": final_score,

        "recommendation": recommendation,

        "overallView": overall_view,

        "positives": positives,

        "risks": risks,

        "metrics": {

            "pe": pe,

            "roe": roe,

            "debtToEquity": debt_to_equity,

            "revenueGrowth": revenue_growth,

            "profitMargin": profit_margin,

            "momentum": round(
                momentum,
                2
            ),

            "rsi": round(
                rsi_value,
                2
            )
        }
    }