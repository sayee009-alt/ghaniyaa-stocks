import { useState } from "react";

function PortfolioCard({
  portfolio,
  onSell,
}) {

  const [sellingStock, setSellingStock] = useState(null);
  const [sellQuantity, setSellQuantity] = useState("");
  const [sellPrice, setSellPrice] = useState("");

  if (!portfolio) {
    return (
      <div className="bg-white p-6 rounded shadow">
        Portfolio is empty.
      </div>
    );
  }

  const totalInvestment =
    Number(portfolio.totalInvestment || 0);

  const currentValue =
    Number(portfolio.currentValue || 0);

  const profit =
    Number(portfolio.profit || 0);

  const realizedProfit =
    Number(portfolio.realizedProfit || 0);

  const totalProfit =
    Number(portfolio.totalProfit || 0);

  const returnPercentage =
    totalInvestment > 0
      ? (profit / totalInvestment) * 100
      : 0;


  // ============================================================
  // OPEN SELL DIALOG
  // ============================================================

  function openSellDialog(stock) {

    setSellingStock(stock);

    setSellQuantity("");

    setSellPrice(
      stock.currentPrice
        ? String(stock.currentPrice)
        : ""
    );
  }


  // ============================================================
  // CLOSE SELL DIALOG
  // ============================================================

  function closeSellDialog() {

    setSellingStock(null);
    setSellQuantity("");
    setSellPrice("");
  }


  // ============================================================
  // CONFIRM SELL
  // ============================================================

  async function handleSell() {

    if (!sellingStock) {
      return;
    }

    const quantity = Number(sellQuantity);
    const price = Number(sellPrice);

    if (!quantity || quantity <= 0) {

      alert(
        "Please enter a valid sell quantity."
      );

      return;
    }

    if (!price || price <= 0) {

      alert(
        "Please enter a valid sell price."
      );

      return;
    }

    if (
      quantity >
      Number(sellingStock.quantity)
    ) {

      alert(
        `You only own ${sellingStock.quantity} shares of ${sellingStock.symbol}.`
      );

      return;
    }

    try {

      console.log(
        "SELL FROM PORTFOLIO DASHBOARD:",
        {
          symbol: sellingStock.symbol,
          quantity,
          sellPrice: price,
        }
      );

      await onSell({

        symbol: sellingStock.symbol,

        quantity: quantity,

        sellPrice: price,

      });

      closeSellDialog();

    } catch (error) {

      console.error(
        "Sell UI Error:",
        error
      );

      alert(
        error.message ||
        "Unable to sell stock."
      );
    }
  }


  return (

    <div className="bg-white p-6 rounded shadow">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-2xl font-bold">
            💼 Portfolio Dashboard
          </h2>

          <p className="text-gray-500 text-sm mt-1">
            Your current investment portfolio
          </p>

        </div>

      </div>


      {/* =====================================================
          SUMMARY
      ===================================================== */}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">


        {/* INVESTMENT */}

        <div className="bg-blue-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Investment
          </h3>

          <p className="text-xl font-bold mt-1">
            ₹{totalInvestment.toFixed(2)}
          </p>

        </div>


        {/* CURRENT VALUE */}

        <div className="bg-green-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Current Value
          </h3>

          <p className="text-xl font-bold mt-1">
            ₹{currentValue.toFixed(2)}
          </p>

        </div>


        {/* UNREALIZED P/L */}

        <div className="bg-yellow-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Unrealized P/L
          </h3>

          <p
            className={`text-xl font-bold mt-1 ${
              profit >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹{profit.toFixed(2)}
          </p>

        </div>


        {/* RETURN */}

        <div className="bg-indigo-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Return
          </h3>

          <p
            className={`text-xl font-bold mt-1 ${
              returnPercentage >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            {returnPercentage.toFixed(2)}%
          </p>

        </div>


        {/* REALIZED P/L */}

        <div className="bg-purple-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Realized P/L
          </h3>

          <p
            className={`text-xl font-bold mt-1 ${
              realizedProfit >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹{realizedProfit.toFixed(2)}
          </p>

        </div>


        {/* TOTAL P/L */}

        <div className="bg-gray-50 p-4 rounded-lg">

          <h3 className="font-semibold text-gray-700">
            Total P/L
          </h3>

          <p
            className={`text-xl font-bold mt-1 ${
              totalProfit >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹{totalProfit.toFixed(2)}
          </p>

        </div>

      </div>


      {/* =====================================================
          HOLDINGS HEADER
      ===================================================== */}

      <div className="flex items-center justify-between mb-3">

        <h3 className="text-xl font-bold">
          Holdings
        </h3>

        <span className="text-sm text-gray-500">
          {portfolio.holdings?.length || 0} stocks
        </span>

      </div>


      {/* =====================================================
          HOLDINGS TABLE
      ===================================================== */}

      <div className="overflow-x-auto">

        <table className="w-full border-collapse">

          <thead>

            <tr className="bg-gray-100">

              <th className="border p-3 text-left">
                Symbol
              </th>

              <th className="border p-3 text-right">
                Qty
              </th>

              <th className="border p-3 text-right">
                Buy Price
              </th>

              <th className="border p-3 text-right">
                Current Price
              </th>

              <th className="border p-3 text-right">
                Investment
              </th>

              <th className="border p-3 text-right">
                Current Value
              </th>

              <th className="border p-3 text-right">
                Profit
              </th>

              <th className="border p-3 text-right">
                Profit %
              </th>

              <th className="border p-3 text-center">
                Action
              </th>

            </tr>

          </thead>


          <tbody>

            {!portfolio.holdings ||
            portfolio.holdings.length === 0 ? (

              <tr>

                <td
                  colSpan="9"
                  className="border p-6 text-center text-gray-500"
                >
                  No holdings in portfolio.
                </td>

              </tr>

            ) : (

              portfolio.holdings.map((stock) => {

                const investment =
                  Number(stock.investment || 0);

                const currentValue =
                  Number(stock.currentValue || 0);

                const stockProfit =
                  Number(stock.profit || 0);

                const stockReturn =
                  investment > 0
                    ? (stockProfit / investment) * 100
                    : 0;

                return (

                  <tr
                    key={stock.symbol}
                    className="hover:bg-gray-50"
                  >

                    {/* SYMBOL */}

                    <td className="border p-3 font-bold">
                      {stock.symbol}
                    </td>


                    {/* QUANTITY */}

                    <td className="border p-3 text-right">
                      {stock.quantity}
                    </td>


                    {/* BUY PRICE */}

                    <td className="border p-3 text-right">
                      ₹{Number(
                        stock.buyPrice || 0
                      ).toFixed(2)}
                    </td>


                    {/* CURRENT PRICE */}

                    <td className="border p-3 text-right">
                      ₹{Number(
                        stock.currentPrice || 0
                      ).toFixed(2)}
                    </td>


                    {/* INVESTMENT */}

                    <td className="border p-3 text-right">
                      ₹{investment.toFixed(2)}
                    </td>


                    {/* CURRENT VALUE */}

                    <td className="border p-3 text-right">
                      ₹{currentValue.toFixed(2)}
                    </td>


                    {/* PROFIT */}

                    <td
                      className={`border p-3 text-right font-semibold ${
                        stockProfit >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      ₹{stockProfit.toFixed(2)}
                    </td>


                    {/* PROFIT % */}

                    <td
                      className={`border p-3 text-right font-semibold ${
                        stockReturn >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {stockReturn.toFixed(2)}%
                    </td>


                    {/* =================================================
                        SELL BUTTON
                    ================================================= */}

                    <td className="border p-3 text-center">

                      <button
                        type="button"
                        onClick={() =>
                          openSellDialog(stock)
                        }
                        className="bg-red-600 text-white px-4 py-1.5 rounded hover:bg-red-700 transition"
                      >
                        Sell
                      </button>

                    </td>

                  </tr>

                );

              })

            )}

          </tbody>

        </table>

      </div>


      {/* =====================================================
          SELL DIALOG
      ===================================================== */}

      {sellingStock && (

        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">

          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">

            <h2 className="text-2xl font-bold mb-4">
              Sell {sellingStock.symbol}
            </h2>


            <p className="text-gray-600 mb-5">

              You currently own{" "}

              <strong>
                {sellingStock.quantity}
              </strong>{" "}

              shares of{" "}

              <strong>
                {sellingStock.symbol}
              </strong>.

            </p>


            {/* SELL QUANTITY */}

            <label className="block font-semibold mb-1">
              Quantity to Sell
            </label>

            <input
              type="number"
              min="1"
              max={sellingStock.quantity}
              step="1"
              value={sellQuantity}
              onChange={(e) => {

                const value = e.target.value;

                if (
                  value === "" ||
                  /^\d+$/.test(value)
                ) {
                  setSellQuantity(value);
                }

              }}
              placeholder="Enter quantity"
              className="border p-2 rounded w-full mb-4"
            />


            {/* SELL PRICE */}

            <label className="block font-semibold mb-1">
              Sell Price
            </label>

            <input
              type="number"
              min="0.01"
              step="0.01"
              value={sellPrice}
              onChange={(e) =>
                setSellPrice(e.target.value)
              }
              placeholder="Enter sell price"
              className="border p-2 rounded w-full mb-6"
            />


            {/* BUTTONS */}

            <div className="flex justify-end gap-3">

              <button
                type="button"
                onClick={closeSellDialog}
                className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400"
              >
                Cancel
              </button>


              <button
                type="button"
                onClick={handleSell}
                disabled={
                  !sellQuantity ||
                  !sellPrice
                }
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400"
              >
                Confirm Sell
              </button>

            </div>

          </div>

        </div>

      )}

    </div>

  );
}

export default PortfolioCard;