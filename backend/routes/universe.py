from fastapi import APIRouter

from backend.services.universe_manager import (
    validate_current_universe,
    discover_nse_stocks,
)

router = APIRouter()


# -----------------------------------------
# TEST CURRENT UNIVERSE
# -----------------------------------------

@router.get("/universe/test")
def test_universe():
    return validate_current_universe()


# -----------------------------------------
# DISCOVER NSE STOCKS
# -----------------------------------------

@router.get("/universe/discover")
def discover_universe():

    stocks = discover_nse_stocks()

    return {
        "count": len(stocks),
        "stocks": stocks
    }


# -----------------------------------------
# UNIVERSE SUMMARY
# -----------------------------------------

@router.get("/universe")
def get_universe():

    stocks = validate_current_universe()

    valid_stocks = [
        stock
        for stock in stocks
        if stock.get("valid") is True
    ]

    invalid_stocks = [
        stock
        for stock in stocks
        if stock.get("valid") is False
    ]

    return {
        "total": len(stocks),
        "valid": len(valid_stocks),
        "invalid": len(invalid_stocks),
        "stocks": stocks
    }