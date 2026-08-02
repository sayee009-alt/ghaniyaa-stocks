from fastapi import APIRouter
from services.screener import screen_all_stocks

router = APIRouter()


@router.get("/screener")
def screener():
    return screen_all_stocks()