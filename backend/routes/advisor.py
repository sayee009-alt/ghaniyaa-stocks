from fastapi import APIRouter
from backend.routes.portfolio import load_portfolio
import yfinance as yf

router = APIRouter()


@router.get("/advisor")
def advisor():

    holdings = load_portfolio()

    total_holdings = len(holdings)

    # --------------------------------
    # Empty Portfolio
    # --------------------------------

    if total_holdings == 0:
        return {
            "health_score": 0,
            "risk": "Unknown",
            "portfolio_risk_score": 0,
            "portfolio_risk": "Unknown",
            "largest_holding": "Unknown",
            "largest_holding_percent": 0,
            "diversification": "No Portfolio",
            "total_holdings": 0,
            "total_investment": 0,
            "current_value": 0,
            "profit": 0,
            "profit_percent": 0,
            "sector_count": 0,
            "sector_diversification_score": 0,
            "sectors": {},
            "recommendation": "Add stocks to begin analysis."
        }

    # --------------------------------
    # Initialize
    # --------------------------------

    total_investment = 0
    current_value = 0

    sectors = {}

    # --------------------------------
    # Analyze Holdings
    # --------------------------------

    for item in holdings:

        symbol = item["symbol"].upper()
        quantity = float(item["quantity"])
        buy_price = float(item["buyPrice"])

        investment = quantity * buy_price

        total_investment += investment

        current_price = buy_price
        sector = "Unknown"

        try:

            stock = yf.Ticker(symbol + ".NS")

            # Get latest price
            history = stock.history(period="1d")

            if not history.empty:

                close_prices = history["Close"].dropna()

                if not close_prices.empty:
                    current_price = float(
                        close_prices.iloc[-1]
                    )

            # Get sector
            try:

                info = stock.info

                sector = info.get(
                    "sector",
                    "Unknown"
                )

                if not sector:
                    sector = "Unknown"

            except Exception:

                sector = "Unknown"

        except Exception as e:

            print(
                f"Advisor error for {symbol}: {e}"
            )

            current_price = buy_price
            sector = "Unknown"

        # --------------------------------
        # Current Value
        # --------------------------------

        value = quantity * current_price

        current_value += value

        # --------------------------------
        # Sector Value
        # --------------------------------

        sectors[sector] = (
            sectors.get(sector, 0) + value
        )

    # --------------------------------
    # Profit
    # --------------------------------

    profit = current_value - total_investment

    if total_investment > 0:

        profit_percent = (
            profit / total_investment
        ) * 100

    else:

        profit_percent = 0

    # --------------------------------
    # Sector Percentages
    # --------------------------------

    sector_percentages = {}

    for sector, value in sectors.items():

        if current_value > 0:

            percentage = (
                value / current_value
            ) * 100

        else:

            percentage = 0

        sector_percentages[sector] = round(
            percentage,
            2
        )

    sector_count = len(
        sector_percentages
    )

    # --------------------------------
    # Largest Sector
    # --------------------------------

    largest_sector = None
    largest_percentage = 0

    for sector, percentage in sector_percentages.items():

        if percentage > largest_percentage:

            largest_percentage = percentage
            largest_sector = sector

    # --------------------------------
    # Sector Diversification Score
    # --------------------------------

    if sector_count == 0:

        sector_diversification_score = 0

    elif largest_percentage >= 90:

        sector_diversification_score = 20

    elif largest_percentage >= 70:

        sector_diversification_score = 40

    elif largest_percentage >= 50:

        sector_diversification_score = 60

    elif largest_percentage >= 40:

        sector_diversification_score = 75

    else:

        sector_diversification_score = 90

    # --------------------------------
    # Portfolio Risk Analysis
    # --------------------------------

    portfolio_risk_score = 100

    # --------------------------------
    # Largest Holding
    # --------------------------------

    largest_holding_value = 0
    largest_holding_symbol = "Unknown"

    for item in holdings:

        symbol = item["symbol"].upper()
        quantity = float(item["quantity"])
        buy_price = float(item["buyPrice"])

        holding_value = (
            quantity * buy_price
        )

        if holding_value > largest_holding_value:

            largest_holding_value = holding_value
            largest_holding_symbol = symbol

    # --------------------------------
    # Largest Holding Percentage
    # --------------------------------

    if total_investment > 0:

        largest_holding_percentage = (
            largest_holding_value
            / total_investment
        ) * 100

    else:

        largest_holding_percentage = 0

    # --------------------------------
    # Holding Concentration Penalty
    # --------------------------------

    if largest_holding_percentage >= 75:

        portfolio_risk_score -= 40

    elif largest_holding_percentage >= 60:

        portfolio_risk_score -= 30

    elif largest_holding_percentage >= 40:

        portfolio_risk_score -= 20

    elif largest_holding_percentage >= 30:

        portfolio_risk_score -= 10

    # --------------------------------
    # Sector Concentration Penalty
    # --------------------------------

    if sector_count == 1:

        portfolio_risk_score -= 30

    elif sector_count == 2:

        portfolio_risk_score -= 15

    elif sector_count == 3:

        portfolio_risk_score -= 5

    # --------------------------------
    # Number of Holdings Penalty
    # --------------------------------

    if total_holdings == 1:

        portfolio_risk_score -= 20

    elif total_holdings == 2:

        portfolio_risk_score -= 10

    elif total_holdings < 5:

        portfolio_risk_score -= 5

    # --------------------------------
    # Final Portfolio Risk Score
    # --------------------------------

    portfolio_risk_score = max(
        0,
        min(
            100,
            portfolio_risk_score
        )
    )

    # --------------------------------
    # Portfolio Risk Classification
    # --------------------------------

    if portfolio_risk_score >= 80:

        portfolio_risk = "Low"

    elif portfolio_risk_score >= 60:

        portfolio_risk = "Medium"

    elif portfolio_risk_score >= 40:

        portfolio_risk = "High"

    else:

        portfolio_risk = "Very High"

    # --------------------------------
    # Diversification
    # --------------------------------

    if sector_count == 0:

        diversification = "Unknown"

    elif sector_count == 1:

        diversification = "Very Low"

    elif sector_count == 2:

        diversification = "Low"

    elif sector_count < 4:

        diversification = "Basic"

    elif sector_count < 6:

        diversification = "Good"

    else:

        diversification = "Strong"

    # --------------------------------
    # Health Score
    # --------------------------------

    health_score = 100

    # Number of holdings
    if total_holdings < 3:

        health_score -= 20

    elif total_holdings < 5:

        health_score -= 10

    # Sector diversification
    if sector_count == 1:

        health_score -= 20

    elif sector_count == 2:

        health_score -= 10

    # Negative performance
    if profit_percent < 0:

        health_score -= 10

    if profit_percent < -10:

        health_score -= 10

    # Sector diversification score
    if sector_diversification_score < 40:

        health_score -= 20

    elif sector_diversification_score < 60:

        health_score -= 15

    elif sector_diversification_score < 75:

        health_score -= 10

    health_score = max(
        0,
        min(
            100,
            health_score
        )
    )

    # --------------------------------
    # Overall Risk
    # --------------------------------

    if health_score >= 85:

        risk = "Low"

    elif health_score >= 70:

        risk = "Medium"

    else:

        risk = "High"

    # --------------------------------
    # Recommendation
    # --------------------------------

    if sector_count == 1:

        recommendation = (
            f"Your portfolio is completely "
            f"concentrated in {largest_sector}. "
            f"Consider adding stocks from "
            f"other sectors."
        )

    elif largest_percentage > 60:

        recommendation = (
            f"Your portfolio is heavily "
            f"concentrated in {largest_sector} "
            f"({largest_percentage}%). "
            f"Consider adding stocks from "
            f"other sectors."
        )

    elif sector_count < 3:

        recommendation = (
            "Your portfolio has limited "
            "sector diversification. "
            "Consider adding Banking, Pharma, "
            "FMCG and Energy stocks."
        )

    elif sector_count < 5:

        recommendation = (
            "Your portfolio has reasonable "
            "diversification. Consider monitoring "
            "sector concentration."
        )

    else:

        recommendation = (
            "Your portfolio has strong sector "
            "diversification. Continue monitoring "
            "portfolio performance."
        )

    # --------------------------------
    # Final Response
    # --------------------------------

    return {

        "health_score": health_score,

        "risk": risk,

        "portfolio_risk_score": (
            portfolio_risk_score
        ),

        "portfolio_risk": (
            portfolio_risk
        ),

        "largest_holding": (
            largest_holding_symbol
        ),

        "largest_holding_percent": round(
            largest_holding_percentage,
            2
        ),

        "diversification": (
            diversification
        ),

        "total_holdings": (
            total_holdings
        ),

        "total_investment": round(
            total_investment,
            2
        ),

        "current_value": round(
            current_value,
            2
        ),

        "profit": round(
            profit,
            2
        ),

        "profit_percent": round(
            profit_percent,
            2
        ),

        "sector_count": (
            sector_count
        ),

        "sector_diversification_score": (
            sector_diversification_score
        ),

        "sectors": (
            sector_percentages
        ),

        "recommendation": (
            recommendation
        )
    }