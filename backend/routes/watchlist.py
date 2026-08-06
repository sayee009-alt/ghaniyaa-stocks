import json
from pathlib import Path

# Project root (Ghaniyaa-Stocks)
BASE_DIR = Path(__file__).resolve().parents[2]

WATCHLIST_FILE = BASE_DIR / "database" / "watchlist.json"


def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_watchlist(data):
    WATCHLIST_FILE.parent.mkdir(exist_ok=True)

    with open(WATCHLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)