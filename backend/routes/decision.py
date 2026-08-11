from fastapi import APIRouter
import yfinance as yf
import pandas as pd
import math

from backend.services.yahoo_symbol_service import get_yahoo_symbol

router = APIRouter()


# ============================================================
# Helper Functions
# ============================================================

def safe_number(value, default=0):

    try:

        if value is None:
            return default

        value = float(value)

        if math.isnan(value) or math.isinf(value):
            return default

        return value

    except Exception:

        return default


def clamp(value, minimum=0, maximum=100):

    return max(
        minimum,
        min(maximum, value)
    )


# ============================================================
# Decision Engine
# ============================================================

@router.get("/decision/{symbol}")
def get_decision(symbol: str):

    symbol = symbol.upper().strip()

    # --------------------------------------------------------
    # GET MARKET DATA
    # --------------------------------------------------------

    try:

        stock = yf.Ticker(
    get_yahoo_symbol(symbol)
)

        history = stock.history(
            period="6mo",
            auto_adjust=False
        )

    except Exception as e:

        print(
            f"Decision market data error for {symbol}: {e}"
        )

        return {
            "error": "Unable to retrieve market data",
            "symbol": symbol
        }

    # --------------------------------------------------------
    # Validate History
    # --------------------------------------------------------

    if history.empty:

        return {
            "error": "No market data found",
            "symbol": symbol
        }

    if "Close" not in history.columns:

        return {
            "error": "No closing price available",
            "symbol": symbol
        }

    close = history["Close"].dropna()

    if close.empty:

        return {
            "error": "No closing price available",
            "symbol": symbol
        }

    current_price = safe_number(
        close.iloc[-1]
    )

    # --------------------------------------------------------
    # Technical Indicators
    # --------------------------------------------------------

    ma20_series = close.rolling(20).mean()

    ma50_series = close.rolling(50).mean()

    ma20 = safe_number(
        ma20_series.iloc[-1],
        current_price
    )

    ma50 = safe_number(
        ma50_series.iloc[-1],
        current_price
    )

    # --------------------------------------------------------
    # Momentum
    # --------------------------------------------------------

    if len(close) >= 21:

        previous_price = safe_number(
            close.iloc[-21],
            current_price
        )

        if previous_price > 0:

            momentum = (
                (
                    current_price
                    / previous_price
                ) - 1
            ) * 100

        else:

            momentum = 0

    else:

        momentum = 0

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    delta = close.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (
        100 / (1 + rs)
    )

    rsi_value = safe_number(
        rsi.iloc[-1],
        50
    )

    # ========================================================
    # TECHNICAL SCORE
    # ========================================================

    technical_score = 50

    technical_signals = []

    # --------------------------------------------------------
    # Price vs MA20
    # --------------------------------------------------------

    if current_price > ma20:

        technical_score += 10

        technical_signals.append(
            "Price is above the 20-day moving average."
        )

    else:

        technical_score -= 10

        technical_signals.append(
            "Price is below the 20-day moving average."
        )

    # --------------------------------------------------------
    # MA20 vs MA50
    # --------------------------------------------------------

    if ma20 > ma50:

        technical_score += 15

        technical_signals.append(
            "Short-term trend is above the 50-day trend."
        )

    else:

        technical_score -= 15

        technical_signals.append(
            "Short-term trend is below the 50-day trend."
        )

    # --------------------------------------------------------
    # Momentum
    # --------------------------------------------------------

    if momentum > 5:

        technical_score += 10

        technical_signals.append(
            "Momentum is positive."
        )

    elif momentum < -5:

        technical_score -= 10

        technical_signals.append(
            "Momentum is negative."
        )

    else:

        technical_signals.append(
            "Momentum is relatively neutral."
        )

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    if rsi_value < 30:

        technical_score += 5

        technical_signals.append(
            "RSI indicates potentially oversold conditions."
        )

    elif rsi_value > 70:

        technical_score -= 5

        technical_signals.append(
            "RSI indicates potentially overbought conditions."
        )

    else:

        technical_signals.append(
            "RSI is in a relatively neutral range."
        )

    technical_score = round(
        clamp(technical_score)
    )

    # ========================================================
    # FUNDAMENTAL ANALYSIS
    # ========================================================

    try:

        info = stock.info

    except Exception as e:

        print(
            f"Decision fundamental data error for {symbol}: {e}"
        )

        info = {}

    # --------------------------------------------------------
    # Fundamental Metrics
    # --------------------------------------------------------

    pe = info.get(
        "trailingPE"
    )

    roe = info.get(
        "returnOnEquity"
    )

    debt_to_equity = info.get(
        "debtToEquity"
    )

    profit_margin = info.get(
        "profitMargins"
    )

    revenue_growth = info.get(
        "revenueGrowth"
    )

    # Convert safely

    pe_value = safe_number(
        pe,
        0
    )

    roe_value = safe_number(
        roe,
        0
    )

    debt_value = safe_number(
        debt_to_equity,
        0
    )

    profit_margin_value = safe_number(
        profit_margin,
        0
    )

    revenue_growth_value = safe_number(
        revenue_growth,
        0
    )

    # ========================================================
    # FUNDAMENTAL SCORE
    # ========================================================

    fundamental_score = 50

    fundamental_signals = []

    # --------------------------------------------------------
    # PE Ratio
    # --------------------------------------------------------

    if pe is not None:

        if pe_value > 0 and pe_value < 25:

            fundamental_score += 10

            fundamental_signals.append(
                "Valuation appears relatively reasonable based on P/E."
            )

        elif pe_value > 50:

            fundamental_score -= 10

            fundamental_signals.append(
                "P/E indicates a relatively expensive valuation."
            )

        else:

            fundamental_signals.append(
                "P/E valuation is in a moderate range."
            )

    else:

        fundamental_signals.append(
            "P/E data is unavailable."
        )

    # --------------------------------------------------------
    # ROE
    # --------------------------------------------------------

    if roe is not None:

        if roe_value > 0.15:

            fundamental_score += 15

            fundamental_signals.append(
                "Return on equity indicates strong profitability."
            )

        elif roe_value < 0.05:

            fundamental_score -= 10

            fundamental_signals.append(
                "Return on equity is relatively weak."
            )

        else:

            fundamental_signals.append(
                "Return on equity is in a moderate range."
            )

    else:

        fundamental_signals.append(
            "ROE data is unavailable."
        )

    # --------------------------------------------------------
    # Debt
    # --------------------------------------------------------

    if debt_to_equity is not None:

        if debt_value < 100:

            fundamental_score += 10

            fundamental_signals.append(
                "Debt-to-equity appears manageable."
            )

        elif debt_value > 200:

            fundamental_score -= 10

            fundamental_signals.append(
                "Debt-to-equity indicates elevated leverage."
            )

        else:

            fundamental_signals.append(
                "Debt-to-equity is in a moderate range."
            )

    else:

        fundamental_signals.append(
            "Debt-to-equity data is unavailable."
        )

    # --------------------------------------------------------
    # Profit Margin
    # --------------------------------------------------------

    if profit_margin is not None:

        if profit_margin_value > 0.15:

            fundamental_score += 5

            fundamental_signals.append(
                "Profit margin indicates healthy profitability."
            )

        elif profit_margin_value < 0:

            fundamental_score -= 5

            fundamental_signals.append(
                "The company currently has negative profit margins."
            )

    # --------------------------------------------------------
    # Revenue Growth
    # --------------------------------------------------------

    if revenue_growth is not None:

        if revenue_growth_value > 0.10:

            fundamental_score += 5

            fundamental_signals.append(
                "Revenue growth is positive."
            )

        elif revenue_growth_value < 0:

            fundamental_score -= 5

            fundamental_signals.append(
                "Revenue growth is negative."
            )

    fundamental_score = round(
        clamp(fundamental_score)
    )

    # ========================================================
    # FINAL GHANIYAA DECISION SCORE
    # ========================================================

    final_score = round(
        (
            fundamental_score * 0.60
            +
            technical_score * 0.40
        )
    )

    final_score = round(
        clamp(final_score)
    )

    # ========================================================
    # DECISION
    # ========================================================

    if final_score >= 75:

        recommendation = "BUY"

    elif final_score >= 55:

        recommendation = "HOLD"

    else:

        recommendation = "SELL"

    # ========================================================
    # CONFIDENCE
    # ========================================================

    score_distance = abs(
        final_score - 50
    )

    confidence = 50 + (
        score_distance * 1.5
    )

    confidence = round(
        clamp(
            confidence,
            50,
            95
        )
    )

    # ========================================================
    # DECISION STRENGTH
    # ========================================================

    if final_score >= 80:

        decision_strength = "Strong"

    elif final_score >= 70:

        decision_strength = "Moderate"

    elif final_score >= 55:

        decision_strength = "Neutral"

    elif final_score >= 40:

        decision_strength = "Weak"

    else:

        decision_strength = "Strong"

    # ========================================================
    # POSITIVE / NEGATIVE SIGNALS
    # ========================================================

    positive_signals = []

    negative_signals = []

    # --------------------------------------------------------
    # Technical
    # --------------------------------------------------------

    if current_price > ma20:

        positive_signals.append(
            "Price is above the 20-day moving average."
        )

    else:

        negative_signals.append(
            "Price is below the 20-day moving average."
        )

    if ma20 > ma50:

        positive_signals.append(
            "20-day moving average is above the 50-day moving average."
        )

    else:

        negative_signals.append(
            "20-day moving average is below the 50-day moving average."
        )

    if momentum > 5:

        positive_signals.append(
            "Positive price momentum."
        )

    elif momentum < -5:

        negative_signals.append(
            "Negative price momentum."
        )

    if rsi_value < 30:

        positive_signals.append(
            "RSI suggests potentially oversold conditions."
        )

    elif rsi_value > 70:

        negative_signals.append(
            "RSI suggests potentially overbought conditions."
        )

    # --------------------------------------------------------
    # Fundamentals
    # --------------------------------------------------------

    if roe_value > 0.15:

        positive_signals.append(
            "Strong return on equity."
        )

    elif roe is not None and roe_value < 0.05:

        negative_signals.append(
            "Weak return on equity."
        )

    if debt_to_equity is not None:

        if debt_value < 100:

            positive_signals.append(
                "Manageable debt-to-equity."
            )

        elif debt_value > 200:

            negative_signals.append(
                "High debt-to-equity."
            )

    if pe is not None:

        if pe_value > 0 and pe_value < 25:

            positive_signals.append(
                "Relatively reasonable P/E valuation."
            )

        elif pe_value > 50:

            negative_signals.append(
                "High P/E valuation."
            )

    if revenue_growth is not None:

        if revenue_growth_value > 0.10:

            positive_signals.append(
                "Positive revenue growth."
            )

        elif revenue_growth_value < 0:

            negative_signals.append(
                "Negative revenue growth."
            )

    # ========================================================
    # Decision Explanation
    # ========================================================

    if recommendation == "BUY":

        decision_reason = (
            "The combined fundamental and technical analysis "
            "shows a positive setup. The stock's strengths "
            "currently outweigh the identified risks."
        )

    elif recommendation == "HOLD":

        decision_reason = (
            "The analysis shows a mixed or moderate setup. "
            "The stock may have strengths, but the current "
            "signals are not strong enough for a clear BUY "
            "or SELL decision."
        )

    else:

        decision_reason = (
            "The combined analysis shows weakness. "
            "Negative fundamental or technical signals "
            "currently outweigh the positive signals."
        )

    # ========================================================
    # Investor Risk Note
    # ========================================================

    if recommendation == "BUY":

        risk_note = (
            "BUY does not mean the stock is guaranteed to rise. "
            "Monitor valuation, business fundamentals and market conditions."
        )

    elif recommendation == "HOLD":

        risk_note = (
            "HOLD indicates that the current signals are mixed. "
            "Monitor future earnings, valuation and technical trends."
        )

    else:

        risk_note = (
            "SELL indicates weakness in the current model signals. "
            "Review the company's fundamentals before making an investment decision."
        )

    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "symbol": symbol,

        "company": info.get(
            "longName",
            symbol
        ),

        "currentPrice": round(
            current_price,
            2
        ),

        # ----------------------------------------------------
        # Scores
        # ----------------------------------------------------

        "fundamentalScore": fundamental_score,

        "technicalScore": technical_score,

        "finalScore": final_score,

        "confidence": confidence,

        # ----------------------------------------------------
        # Decision
        # ----------------------------------------------------

        "recommendation": recommendation,

        "decisionStrength": decision_strength,

        "decisionReason": decision_reason,

        # ----------------------------------------------------
        # Technical Indicators
        # ----------------------------------------------------

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
        },

        # ----------------------------------------------------
        # Fundamental Indicators
        # ----------------------------------------------------

        "fundamentals": {

            "pe": (
                round(pe_value, 2)
                if pe is not None
                else None
            ),

            "roe": (
                round(
                    roe_value * 100,
                    2
                )
                if roe is not None
                else None
            ),

            "debtToEquity": (
                round(
                    debt_value,
                    2
                )
                if debt_to_equity is not None
                else None
            ),

            "profitMargin": (
                round(
                    profit_margin_value * 100,
                    2
                )
                if profit_margin is not None
                else None
            ),

            "revenueGrowth": (
                round(
                    revenue_growth_value * 100,
                    2
                )
                if revenue_growth is not None
                else None
            )
        },

        # ----------------------------------------------------
        # Signals
        # ----------------------------------------------------

        "positiveSignals": positive_signals,

        "negativeSignals": negative_signals,

        "technicalSignals": technical_signals,

        "fundamentalSignals": fundamental_signals,

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        "riskNote": risk_note
    }