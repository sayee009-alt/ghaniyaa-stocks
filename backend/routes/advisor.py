from fastapi import APIRouter
from backend.routes.portfolio import load_portfolio
import yfinance as yf

router = APIRouter()


@router.get("/advisor")
def advisor():

    holdings = load_portfolio()

    total_holdings = len(holdings)

    # ============================================================
    # EMPTY PORTFOLIO
    # ============================================================

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

            "recommendation": (
                "Add stocks to begin portfolio analysis."
            )
        }

    # ============================================================
    # INITIALIZE
    # ============================================================

    total_investment = 0
    current_value = 0

    sectors = {}

    # ============================================================
    # ANALYZE HOLDINGS
    # ============================================================

    for item in holdings:

        symbol = item["symbol"].upper()

        quantity = float(
            item["quantity"]
        )

        buy_price = float(
            item["buyPrice"]
        )

        # --------------------------------------------------------
        # Investment
        # --------------------------------------------------------

        investment = quantity * buy_price

        total_investment += investment

        # --------------------------------------------------------
        # Default values
        # --------------------------------------------------------

        current_price = buy_price
        sector = "Unknown"

        # --------------------------------------------------------
        # Yahoo Finance
        # --------------------------------------------------------

        try:

            stock = yf.Ticker(
                symbol + ".NS"
            )

            # ----------------------------------------------------
            # Latest price
            # ----------------------------------------------------

            try:

                history = stock.history(
                    period="1d"
                )

                if not history.empty:

                    close_prices = (
                        history["Close"]
                        .dropna()
                    )

                    if not close_prices.empty:

                        current_price = float(
                            close_prices.iloc[-1]
                        )

            except Exception as e:

                print(
                    f"Price error for {symbol}: {e}"
                )

                current_price = buy_price

            # ----------------------------------------------------
            # Sector
            # ----------------------------------------------------

            try:

                info = stock.info

                sector = info.get(
                    "sector",
                    "Unknown"
                )

                if not sector:
                    sector = "Unknown"

            except Exception as e:

                print(
                    f"Sector error for {symbol}: {e}"
                )

                sector = "Unknown"

        except Exception as e:

            print(
                f"Advisor Yahoo error for {symbol}: {e}"
            )

            current_price = buy_price
            sector = "Unknown"

        # ========================================================
        # CURRENT VALUE
        # ========================================================

        value = quantity * current_price

        current_value += value

        # ========================================================
        # SECTOR VALUE
        # ========================================================

        sectors[sector] = (
            sectors.get(sector, 0) + value
        )

    # ============================================================
    # PORTFOLIO PERFORMANCE
    # ============================================================

    profit = (
        current_value -
        total_investment
    )

    if total_investment > 0:

        profit_percent = (
            profit /
            total_investment
        ) * 100

    else:

        profit_percent = 0

    # ============================================================
    # SECTOR PERCENTAGES
    # ============================================================

    sector_percentages = {}

    for sector, value in sectors.items():

        if current_value > 0:

            percentage = (
                value /
                current_value
            ) * 100

        else:

            percentage = 0

        sector_percentages[sector] = round(
            percentage,
            2
        )

    # ============================================================
    # SECTOR COUNT
    # ============================================================

    sector_count = len(
        sector_percentages
    )

    # ============================================================
    # LARGEST SECTOR
    # ============================================================

    largest_sector = "Unknown"
    largest_sector_percentage = 0

    for sector, percentage in (
        sector_percentages.items()
    ):

        if percentage > largest_sector_percentage:

            largest_sector_percentage = percentage

            largest_sector = sector

    # ============================================================
    # LARGEST HOLDING
    # ============================================================

    largest_holding_value = 0
    largest_holding_symbol = "Unknown"

    for item in holdings:

        symbol = item["symbol"].upper()

        quantity = float(
            item["quantity"]
        )

        buy_price = float(
            item["buyPrice"]
        )

        holding_value = (
            quantity *
            buy_price
        )

        if holding_value > largest_holding_value:

            largest_holding_value = (
                holding_value
            )

            largest_holding_symbol = symbol

    # ============================================================
    # LARGEST HOLDING %
    # ============================================================

    if total_investment > 0:

        largest_holding_percentage = (
            largest_holding_value /
            total_investment
        ) * 100

    else:

        largest_holding_percentage = 0

    # ============================================================
    # DIVERSIFICATION SCORE
    #
    # 0   = Very Poor
    # 100 = Excellent
    # ============================================================

    if sector_count == 0:

        sector_diversification_score = 0

    elif largest_sector_percentage >= 90:

        sector_diversification_score = 20

    elif largest_sector_percentage >= 70:

        sector_diversification_score = 40

    elif largest_sector_percentage >= 50:

        sector_diversification_score = 60

    elif largest_sector_percentage >= 40:

        sector_diversification_score = 75

    else:

        sector_diversification_score = 90

    # ============================================================
    # PORTFOLIO RISK SCORE
    #
    # 0   = Low Risk
    # 100 = Very High Risk
    #
    # IMPORTANT:
    # This is now a TRUE risk score.
    # ============================================================

    portfolio_risk_score = 0

    # ============================================================
    # HOLDING CONCENTRATION
    # ============================================================

    if largest_holding_percentage >= 75:

        portfolio_risk_score += 40

    elif largest_holding_percentage >= 60:

        portfolio_risk_score += 30

    elif largest_holding_percentage >= 40:

        portfolio_risk_score += 20

    elif largest_holding_percentage >= 30:

        portfolio_risk_score += 10

    # ============================================================
    # SECTOR CONCENTRATION
    # ============================================================

    if sector_count == 1:

        portfolio_risk_score += 30

    elif sector_count == 2:

        portfolio_risk_score += 15

    elif sector_count == 3:

        portfolio_risk_score += 5

    # ============================================================
    # NUMBER OF HOLDINGS
    # ============================================================

    if total_holdings == 1:

        portfolio_risk_score += 20

    elif total_holdings == 2:

        portfolio_risk_score += 10

    elif total_holdings < 5:

        portfolio_risk_score += 5

    # ============================================================
    # CAP RISK SCORE
    # ============================================================

    portfolio_risk_score = max(
        0,
        min(
            100,
            portfolio_risk_score
        )
    )

    # ============================================================
    # PORTFOLIO RISK CLASSIFICATION
    # ============================================================

    if portfolio_risk_score <= 20:

        portfolio_risk = "Low"

    elif portfolio_risk_score <= 40:

        portfolio_risk = "Medium"

    elif portfolio_risk_score <= 60:

        portfolio_risk = "High"

    else:

        portfolio_risk = "Very High"

    # ============================================================
    # DIVERSIFICATION LABEL
    # ============================================================

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

    # ============================================================
    # PORTFOLIO HEALTH SCORE
    #
    # 100 = Excellent
    # 0   = Very Weak
    # ============================================================

    health_score = 100

    # ------------------------------------------------------------
    # Number of holdings
    # ------------------------------------------------------------

    if total_holdings == 1:

        health_score -= 20

    elif total_holdings == 2:

        health_score -= 10

    elif total_holdings < 5:

        health_score -= 5

    # ------------------------------------------------------------
    # Sector diversification
    # ------------------------------------------------------------

    if sector_count == 1:

        health_score -= 20

    elif sector_count == 2:

        health_score -= 10

    # ------------------------------------------------------------
    # Largest holding concentration
    # ------------------------------------------------------------

    if largest_holding_percentage >= 75:

        health_score -= 25

    elif largest_holding_percentage >= 60:

        health_score -= 20

    elif largest_holding_percentage >= 40:

        health_score -= 10

    elif largest_holding_percentage >= 30:

        health_score -= 5

    # ------------------------------------------------------------
    # Diversification score
    # ------------------------------------------------------------

    if sector_diversification_score < 40:

        health_score -= 20

    elif sector_diversification_score < 60:

        health_score -= 15

    elif sector_diversification_score < 75:

        health_score -= 10

    # ------------------------------------------------------------
    # Negative performance
    # ------------------------------------------------------------

    if profit_percent < 0:

        health_score -= 10

    if profit_percent < -10:

        health_score -= 10

    # ============================================================
    # LIMIT HEALTH SCORE
    # ============================================================

    health_score = max(
        0,
        min(
            100,
            health_score
        )
    )

    # ============================================================
    # OVERALL HEALTH RISK
    #
    # This is separate from portfolio_risk.
    # ============================================================

    if health_score >= 80:

        risk = "Low"

    elif health_score >= 60:

        risk = "Medium"

    else:

        risk = "High"

    # ============================================================
    # RECOMMENDATION
    # ============================================================

    if (
        largest_holding_percentage >= 75
        and sector_count == 1
    ):

        recommendation = (
            f"{largest_holding_symbol} represents "
            f"{round(largest_holding_percentage, 2)}% "
            f"of your portfolio and your portfolio "
            f"is concentrated in a single sector "
            f"({largest_sector}). This creates "
            f"significant concentration risk. "
            f"Consider gradually diversifying across "
            f"other quality companies and sectors."
        )

    elif largest_holding_percentage >= 60:

        recommendation = (
            f"{largest_holding_symbol} represents "
            f"{round(largest_holding_percentage, 2)}% "
            f"of your portfolio. This creates "
            f"significant concentration risk. "
            f"Consider gradually reducing dependence "
            f"on this holding."
        )

    elif sector_count == 1:

        recommendation = (
            f"Your portfolio is completely "
            f"concentrated in {largest_sector}. "
            f"Consider adding quality companies "
            f"from other sectors."
        )

    elif sector_count == 2:

        recommendation = (
            "Your portfolio is concentrated "
            "across only two sectors. Consider "
            "gradually adding exposure to other "
            "sectors."
        )

    elif sector_count < 4:

        recommendation = (
            "Your portfolio has reasonable "
            "diversification, but adding exposure "
            "to additional sectors could further "
            "reduce concentration risk."
        )

    else:

        recommendation = (
            "Your portfolio has good sector "
            "diversification. Continue monitoring "
            "position sizes, risk and long-term "
            "portfolio performance."
        )

    # ============================================================
    # FINAL RESPONSE
    # ============================================================

    return {

        # --------------------------------------------------------
        # Health
        # --------------------------------------------------------

        "health_score": health_score,

        "risk": risk,

        # --------------------------------------------------------
        # Risk
        # --------------------------------------------------------

        "portfolio_risk_score": (
            portfolio_risk_score
        ),

        "portfolio_risk": (
            portfolio_risk
        ),

        # --------------------------------------------------------
        # Concentration
        # --------------------------------------------------------

        "largest_holding": (
            largest_holding_symbol
        ),

        "largest_holding_percent": round(
            largest_holding_percentage,
            2
        ),

        # --------------------------------------------------------
        # Diversification
        # --------------------------------------------------------

        "diversification": (
            diversification
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

        # --------------------------------------------------------
        # Holdings
        # --------------------------------------------------------

        "total_holdings": (
            total_holdings
        ),

        # --------------------------------------------------------
        # Performance
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # Recommendation
        # --------------------------------------------------------

        "recommendation": (
            recommendation
        )
    }