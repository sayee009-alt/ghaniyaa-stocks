from fastapi import APIRouter

from backend.services.stock_analysis import (
    get_stock_analysis
)


router = APIRouter()


@router.get("/analysis/{symbol}")
def stock_analysis(symbol: str):

    return get_stock_analysis(symbol)