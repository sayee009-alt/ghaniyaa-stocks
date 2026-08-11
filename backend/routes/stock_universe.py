from fastapi import APIRouter

from backend.services.stock_universe_refresh import (
    refresh_master_universe,
)

router = APIRouter(
    prefix="/stock-universe",
    tags=["Stock Universe"],
)


# ============================================================
# REFRESH MASTER STOCK UNIVERSE
# ============================================================

@router.post("/refresh")
def refresh_stock_universe():
    """
    Refresh the master NSE + BSE stock universe.

    This:
    - downloads NSE listings
    - loads BSE listings
    - merges both sources
    - detects new stocks
    - detects removed/inactive stocks
    - updates master_stock_universe.json
    - generates refresh report
    """

    return refresh_master_universe()


# ============================================================
# HEALTH / STATUS
# ============================================================

@router.get("/refresh/status")
def refresh_status():
    """
    Simple endpoint confirming that the stock-universe
    refresh service is available.
    """

    return {
        "success": True,
        "service": "Ghaniyaa Master Stock Universe",
        "status": "ready",
    }