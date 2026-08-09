from fastapi import APIRouter
from backend.routes.portfolio import load_portfolio

router = APIRouter()


@router.get("/advisor")
def advisor():

    holdings = load_portfolio()

    total = len(holdings)

    if total == 0:
        return {
            "health_score": 0,
            "risk": "Unknown",
            "diversification": "No Portfolio",
            "recommendation": "Add stocks to begin analysis."
        }

    health = 100

    if total < 3:
        health -= 20

    if total < 5:
        health -= 10

    if health >= 85:
        risk = "Low"
    elif health >= 70:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "health_score": health,
        "risk": risk,
        "diversification": "Basic",
        "recommendation": "Consider adding Banking, Pharma, FMCG and Energy sectors."
    }