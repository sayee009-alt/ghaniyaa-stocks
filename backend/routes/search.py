from fastapi import APIRouter
from backend.services.search import search_stock

router = APIRouter()


@router.get("/search/{query}")
def search(query: str):
    return search_stock(query)