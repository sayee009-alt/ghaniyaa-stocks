from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
import yfinance as yf

from backend.services.yahoo_ticker import get_yahoo_ticker

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]

PORTFOLIO_FILE = (
    BASE_DIR
    / "database"
    / "portfolio.json"
)

TRANSACTIONS_FILE = (
    BASE_DIR
    / "database"
    / "portfolio_transactions.json"
)


# ============================================================
# LOAD / SAVE PORTFOLIO
# ============================================================

def load_portfolio():

    try:

        with open(
            PORTFOLIO_FILE,
            "r"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []


def save_portfolio(data):

    with open(
        PORTFOLIO_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# LOAD / SAVE TRANSACTIONS
# ============================================================

def load_transactions():

    try:

        with open(
            TRANSACTIONS_FILE,
            "r"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []


def save_transactions(data):

    with open(
        TRANSACTIONS_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# GET PORTFOLIO
# ============================================================

@router.get("/portfolio")
def get_portfolio():

    portfolio = load_portfolio()

    total_investment = 0
    total_value = 0

    holdings = []

    for item in portfolio:

        symbol = str(
            item.get("symbol", "")
        ).strip().upper()

        quantity = float(
            item.get("quantity", 0)
        )

        buy_price = float(
            item.get("buyPrice", 0)
        )

        # ========================================================
        # IGNORE INVALID PORTFOLIO ENTRIES
        # ========================================================

        if not symbol:
            continue

        if quantity <= 0:
            continue

        if buy_price <= 0:
            continue

        yahoo_symbol = get_yahoo_ticker(symbol)

        # ========================================================
        # YAHOO SYMBOL NOT FOUND
        # ========================================================

        if not yahoo_symbol:

            print(
                f"Portfolio Yahoo symbol not found: {symbol}"
            )

            # Keep the holding visible using buy price
            current_price = buy_price

        else:

            try:

                stock = yf.Ticker(
                    yahoo_symbol
                )

                info = stock.info

                current_price = info.get(
                    "currentPrice"
                )

                # =================================================
                # FALLBACK TO BUY PRICE
                # =================================================

                if current_price is None:

                    current_price = info.get(
                        "regularMarketPrice",
                        buy_price
                    )

            except Exception as error:

                print(
                    f"Portfolio Yahoo error for {symbol}: {error}"
                )

                current_price = buy_price

        investment = (
            quantity
            *
            buy_price
        )

        current_value = (
            quantity
            *
            current_price
        )

        profit = (
            current_value
            -
            investment
        )

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

    # ============================================================
    # REALIZED PROFIT
    # ============================================================

    transactions = load_transactions()

    realized_profit = 0

    for transaction in transactions:

        realized_profit += float(
            transaction.get(
                "profit",
                0
            )
        )

    # ============================================================
    # UNREALIZED PROFIT
    # ============================================================

    unrealized_profit = (
        total_value
        -
        total_investment
    )

    # ============================================================
    # TOTAL PROFIT
    # ============================================================

    total_profit = (
        realized_profit
        +
        unrealized_profit
    )

    return {

        "holdings": holdings,

        "totalInvestment": total_investment,

        "currentValue": total_value,

        "profit": unrealized_profit,

        "realizedProfit": realized_profit,

        "totalProfit": total_profit

    }
# ============================================================
# ADD / BUY PORTFOLIO STOCK
# ============================================================

@router.post("/portfolio")
def add_portfolio(stock: dict):

    portfolio = load_portfolio()

    symbol = stock["symbol"].upper()
    quantity = float(stock["quantity"])
    buy_price = float(stock["buyPrice"])

    if quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero."
        )

    if buy_price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Buy price must be greater than zero."
        )

    for item in portfolio:

        if item["symbol"] == symbol:

            old_qty = float(
                item["quantity"]
            )

            new_qty = quantity

            total_qty = (
                old_qty
                +
                new_qty
            )

            avg_price = (
                (
                    item["buyPrice"]
                    * old_qty
                )
                +
                (
                    buy_price
                    * new_qty
                )
            ) / total_qty

            item["quantity"] = total_qty

            item["buyPrice"] = round(
                avg_price,
                2
            )

            save_portfolio(
                portfolio
            )

            return {
                "message": "Portfolio updated",
                "symbol": symbol,
                "quantity": total_qty,
                "buyPrice": round(
                    avg_price,
                    2
                )
            }

    portfolio.append({

        "symbol": symbol,

        "quantity": quantity,

        "buyPrice": buy_price

    })

    save_portfolio(
        portfolio
    )

    return {

        "message": "Added successfully",

        "symbol": symbol,

        "quantity": quantity,

        "buyPrice": buy_price

    }


# ============================================================
# SELL / REMOVE QUANTITY
# ============================================================

@router.post("/portfolio/sell")
def sell_portfolio(stock: dict):

    portfolio = load_portfolio()

    symbol = stock["symbol"].upper()

    sell_quantity = float(
        stock["quantity"]
    )

    sell_price = float(
        stock["sellPrice"]
    )

    if sell_quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Sell quantity must be greater than zero."
        )

    if sell_price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Sell price must be greater than zero."
        )

    # ========================================================
    # FIND HOLDING
    # ========================================================

    for item in portfolio:

        if item["symbol"] == symbol:

            current_quantity = float(
                item["quantity"]
            )

            average_buy_price = float(
                item["buyPrice"]
            )

            # =================================================
            # CANNOT SELL MORE THAN OWNED
            # =================================================

            if sell_quantity > current_quantity:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Cannot sell {sell_quantity} shares "
                        f"of {symbol}. "
                        f"You only own {current_quantity}."
                    )
                )

            # =================================================
            # REALIZED PROFIT
            # =================================================

            realized_profit = (
                (
                    sell_price
                    -
                    average_buy_price
                )
                *
                sell_quantity
            )

            # =================================================
            # REDUCE HOLDING
            # =================================================

            remaining_quantity = (
                current_quantity
                -
                sell_quantity
            )

            # =================================================
            # SAVE TRANSACTION
            # =================================================

            transactions = load_transactions()

            transactions.append({

                "type": "SELL",

                "symbol": symbol,

                "quantity": sell_quantity,

                "buyPrice": average_buy_price,

                "sellPrice": sell_price,

                "profit": round(
                    realized_profit,
                    2
                )

            })

            save_transactions(
                transactions
            )

            # =================================================
            # IF ALL SHARES SOLD
            # =================================================

            if remaining_quantity <= 0:

                portfolio.remove(item)

            else:

                item["quantity"] = (
                    remaining_quantity
                )

            save_portfolio(
                portfolio
            )

            return {

                "message": "Sale successful",

                "symbol": symbol,

                "soldQuantity": sell_quantity,

                "remainingQuantity": (
                    remaining_quantity
                ),

                "sellPrice": sell_price,

                "realizedProfit": round(
                    realized_profit,
                    2
                )

            }

    # ========================================================
    # SYMBOL NOT FOUND
    # ========================================================

    raise HTTPException(
        status_code=404,
        detail=(
            f"{symbol} is not present "
            "in your portfolio."
        )
    )