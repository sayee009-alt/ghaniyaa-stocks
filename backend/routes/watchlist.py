import json

WATCHLIST_FILE = "../database/watchlist.json"


def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)