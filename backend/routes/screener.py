from fastapi import APIRouter

from backend.services.screener import screen_all_stocks

router = APIRouter()


@router.get("/screener")
def screener(
    sector: str | None = None,
    min_score: float | None = None,
    sort: str = "score",
    order: str = "desc",
    limit: int | None = None,
):
    return screen_all_stocks(
        sector=sector,
        min_score=min_score,
        sort=sort,
        order=order,
        limit=limit,
    )