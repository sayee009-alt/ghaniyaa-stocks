from fastapi import APIRouter
import yfinance as yf
import pandas as pd

from backend.services.yahoo_symbol_service import get_yahoo_symbol

router = APIRouter()


@router.get("/prediction/{symbol}")
def predict(symbol: str):

    symbol = symbol.strip().upper()

    stock = yf.Ticker(
        get_yahoo_symbol(symbol)
    )

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

    # Moving averages
    ma20 = float(
        close.rolling(20).mean().iloc[-1]
    )

    ma50 = float(
        close.rolling(50).mean().iloc[-1]
    )

    # Momentum
    momentum_20 = (
        float(
            ((current_price / close.iloc[-21]) - 1) * 100
        )
        if len(close) >= 21
        else 0
    )

    # Daily returns
    returns = close.pct_change().dropna()

    # Average return
    avg_return = (
        float(returns.mean())
        if not returns.empty
        else 0
    )

    # Volatility
    volatility = (
        float(returns.std() * 100)
        if not returns.empty
        else 0
    )

    # RSI
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    current_rsi = float(rsi.iloc[-1])

    if pd.isna(current_rsi):
        current_rsi = 50

    # --------------------------------
    # SCORING MODEL
    # --------------------------------

    score = 50

    # Moving average signal
    if current_price > ma20:
        score += 10
    else:
        score -= 10

    if ma20 > ma50:
        score += 15
    else:
        score -= 15

    # Momentum signal
    if momentum_20 > 5:
        score += 10

    elif momentum_20 < -5:
        score -= 10

    # RSI signal
    if current_rsi < 30:
        score += 5

    elif current_rsi > 70:
        score -= 5

    # Keep score between 0 and 100
    score = max(
        0,
        min(100, score)
    )

    # --------------------------------
    # TREND
    # --------------------------------

    if score >= 65:
        trend = "Bullish"

    elif score <= 40:
        trend = "Bearish"

    else:
        trend = "Neutral"

    # --------------------------------
    # RECOMMENDATION
    # --------------------------------

    if score >= 70:
        recommendation = "BUY"

    elif score <= 40:
        recommendation = "SELL"

    else:
        recommendation = "HOLD"

    # --------------------------------
    # PRICE PROJECTION
    # --------------------------------

    predicted_price = (
        current_price * (1 + avg_return)
    )

    if pd.isna(predicted_price):
        predicted_price = current_price

    predicted_price = float(
        predicted_price
    )

    return {
        "symbol": symbol,

        "currentPrice": round(
            current_price,
            2
        ),

        "predictedPrice": round(
            predicted_price,
            2
        ),

        "trend": trend,

        "confidence": score,

        "recommendation": recommendation,

        "signals": {
            "ma20": round(ma20, 2),
            "ma50": round(ma50, 2),
            "momentum20": round(
                momentum_20,
                2
            ),
            "rsi": round(
                current_rsi,
                2
            ),
            "volatility": round(
                volatility,
                2
            )
        }
    }