from fastapi import APIRouter
from backend.services.screener import screen_all_stocks

router = APIRouter()


@router.get("/screener")
def screener():
    return screen_all_stocks()