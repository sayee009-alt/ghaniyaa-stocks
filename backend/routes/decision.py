from fastapi import APIRouter
import yfinance as yf
import pandas as pd

router = APIRouter()


@router.get("/decision/{symbol}")
def get_decision(symbol: str):

    symbol = symbol.upper()

    # -----------------------------
    # GET MARKET DATA
    # -----------------------------

    stock = yf.Ticker(symbol + ".NS")

    history = stock.history(period="6mo")

    if history.empty:
        return {
            "error": "No market data found",
            "symbol": symbol
        }

    close = history["Close"].dropna()

    if close.empty:
        return {
            "error": "No closing price available",
            "symbol": symbol
        }

    current_price = float(close.iloc[-1])

    # -----------------------------
    # TECHNICAL ANALYSIS
    # -----------------------------

    ma20 = float(
        close.rolling(20).mean().iloc[-1]
    )

    ma50 = float(
        close.rolling(50).mean().iloc[-1]
    )

    # Momentum

    if len(close) >= 21:

        momentum = (
            (current_price / float(close.iloc[-21])) - 1
        ) * 100

    else:

        momentum = 0

    # RSI

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    rsi_value = float(rsi.iloc[-1])

    if pd.isna(rsi_value):

        rsi_value = 50

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
    # GHANIYAA SCORE
    # -----------------------------

    info = stock.info

    # Basic fundamental indicators

    pe = info.get("trailingPE")

    roe = info.get("returnOnEquity")

    debt_to_equity = info.get("debtToEquity")

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

    fundamental_score = max(
        0,
        min(100, fundamental_score)
    )

    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = (
        fundamental_score * 0.60
        +
        technical_score * 0.40
    )

    final_score = round(final_score)

    # -----------------------------
    # FINAL DECISION
    # -----------------------------

    if final_score >= 70:

        recommendation = "BUY"

        confidence = min(
            95,
            final_score
        )

    elif final_score >= 50:

        recommendation = "HOLD"

        confidence = final_score

    else:

        recommendation = "SELL"

        confidence = max(
            50,
            final_score
        )

    # -----------------------------
    # RESPONSE
    # -----------------------------

    return {

        "symbol": symbol,

        "currentPrice": round(
            current_price,
            2
        ),

        "fundamentalScore": round(
            fundamental_score
        ),

        "technicalScore": round(
            technical_score
        ),

        "finalScore": final_score,

        "confidence": confidence,

        "recommendation": recommendation,

        "signals": {

            "ma20": round(
                ma20,
                2
            ),

            "ma50": round(
                ma50,
                2
            ),

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