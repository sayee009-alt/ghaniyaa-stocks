from fastapi import APIRouter
import json
from pathlib import Path
import yfinance as yf

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
PORTFOLIO_FILE = BASE_DIR / "database" / "portfolio.json"


def load_portfolio():
    try:
        with open(PORTFOLIO_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(data, file, indent=4)


@router.get("/portfolio")
def get_portfolio():
    portfolio = load_portfolio()

    total_investment = 0
    total_value = 0

    holdings = []

    for item in portfolio:

        symbol = item["symbol"]
        quantity = item["quantity"]
        buy_price = item["buyPrice"]

        stock = yf.Ticker(symbol + ".NS")
        info = stock.info

        current_price = info.get("currentPrice", buy_price)

        investment = quantity * buy_price
        current_value = quantity * current_price
        profit = current_value - investment

        total_investment += investment
        total_value += current_value

        holdings.append({
            "symbol": symbol,
            "quantity": quantity,
            "buyPrice": buy_price,
            "currentPrice": current_price,
            "investment": investment,
            "currentValue": current_value,
            "profit": profit
        })

    return {
        "holdings": holdings,
        "totalInvestment": total_investment,
        "currentValue": total_value,
        "profit": total_value - total_investment
    }


@router.post("/portfolio")
def add_portfolio(stock: dict):

    portfolio = load_portfolio()

    for item in portfolio:

        if item["symbol"] == stock["symbol"]:

            old_qty = item["quantity"]
            new_qty = stock["quantity"]

            total_qty = old_qty + new_qty

            avg_price = (
                item["buyPrice"] * old_qty +
                stock["buyPrice"] * new_qty
            ) / total_qty

            item["quantity"] = total_qty
            item["buyPrice"] = round(avg_price, 2)

            save_portfolio(portfolio)

            return {
                "message": "Portfolio updated"
            }

    portfolio.append(stock)

    save_portfolio(portfolio)

    return {
        "message": "Added successfully"
    }