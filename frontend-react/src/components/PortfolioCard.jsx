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


  function openSellDialog(stock) {

    setSellingStock(stock);

    setSellQuantity("");

    setSellPrice(
      stock.currentPrice
        ? String(stock.currentPrice)
        : ""
    );

  }


  function closeSellDialog() {

    setSellingStock(null);

    setSellQuantity("");

    setSellPrice("");

  }


  async function handleSell() {

    if (!sellingStock) {
      return;
    }


    const quantity = Number(
      sellQuantity
    );

    const price = Number(
      sellPrice
    );


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

      await onSell({

        symbol:
          sellingStock.symbol,

        quantity:
          quantity,

        sellPrice:
          price,

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

      <h2 className="text-2xl font-bold mb-4">
        💼 Portfolio Dashboard
      </h2>


      {/* =====================================================
          SUMMARY
      ===================================================== */}

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">


        <div className="bg-blue-50 p-4 rounded">

          <h3 className="font-semibold">
            Investment
          </h3>

          <p className="text-xl font-bold">
            ₹
            {portfolio.totalInvestment.toFixed(2)}
          </p>

        </div>


        <div className="bg-green-50 p-4 rounded">

          <h3 className="font-semibold">
            Current Value
          </h3>

          <p className="text-xl font-bold">
            ₹
            {portfolio.currentValue.toFixed(2)}
          </p>

        </div>


        <div className="bg-yellow-50 p-4 rounded">

          <h3 className="font-semibold">
            Unrealized P/L
          </h3>

          <p
            className={`text-xl font-bold ${
              portfolio.profit >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹
            {portfolio.profit.toFixed(2)}
          </p>

        </div>


        <div className="bg-purple-50 p-4 rounded">

          <h3 className="font-semibold">
            Realized P/L
          </h3>

          <p
            className={`text-xl font-bold ${
              (portfolio.realizedProfit || 0) >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹
            {(portfolio.realizedProfit || 0).toFixed(2)}
          </p>

        </div>


        <div className="bg-gray-50 p-4 rounded">

          <h3 className="font-semibold">
            Total P/L
          </h3>

          <p
            className={`text-xl font-bold ${
              (portfolio.totalProfit || 0) >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹
            {(portfolio.totalProfit || 0).toFixed(2)}
          </p>

        </div>

      </div>


      {/* =====================================================
          HOLDINGS TABLE
      ===================================================== */}

      <div className="overflow-x-auto">

        <table className="w-full border">

          <thead className="bg-gray-100">

            <tr>

              <th className="border p-2">
                Symbol
              </th>

              <th className="border p-2">
                Qty
              </th>

              <th className="border p-2">
                Buy
              </th>

              <th className="border p-2">
                Current
              </th>

              <th className="border p-2">
                Investment
              </th>

              <th className="border p-2">
                Value
              </th>

              <th className="border p-2">
                Profit
              </th>

              <th className="border p-2">
                Action
              </th>

            </tr>

          </thead>


          <tbody>

            {portfolio.holdings.length === 0 ? (

              <tr>

                <td
                  colSpan="8"
                  className="border p-4 text-center text-gray-500"
                >
                  No holdings in portfolio.
                </td>

              </tr>

            ) : (

              portfolio.holdings.map(
                (stock) => (

                  <tr
                    key={stock.symbol}
                  >

                    <td className="border p-2">
                      {stock.symbol}
                    </td>


                    <td className="border p-2">
                      {stock.quantity}
                    </td>


                    <td className="border p-2">
                      ₹
                      {stock.buyPrice}
                    </td>


                    <td className="border p-2">
                      ₹
                      {stock.currentPrice}
                    </td>


                    <td className="border p-2">
                      ₹
                      {stock.investment.toFixed(2)}
                    </td>


                    <td className="border p-2">
                      ₹
                      {stock.currentValue.toFixed(2)}
                    </td>


                    <td
                      className={`border p-2 ${
                        stock.profit >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      ₹
                      {stock.profit.toFixed(2)}
                    </td>


                    {/* =================================================
                        SELL BUTTON
                    ================================================= */}

                    <td className="border p-2">

                      <button
                        type="button"
                        onClick={() =>
                          openSellDialog(
                            stock
                          )
                        }
                        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Sell
                      </button>

                    </td>

                  </tr>

                )
              )

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


            <p className="text-gray-600 mb-4">

              You currently own{" "}

              <strong>
                {sellingStock.quantity}
              </strong>{" "}

              shares.

            </p>


            {/* SELL QUANTITY */}

            <label className="block font-semibold mb-1">

              Quantity to Sell

            </label>

            <input
              type="number"
              min="0.000001"
              step="any"
              value={sellQuantity}
              onChange={(e) =>
                setSellQuantity(
                  e.target.value
                )
              }
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
              step="any"
              value={sellPrice}
              onChange={(e) =>
                setSellPrice(
                  e.target.value
                )
              }
              placeholder="Enter sell price"
              className="border p-2 rounded w-full mb-6"
            />


            {/* BUTTONS */}

            <div className="flex justify-end gap-3">

              <button
                type="button"
                onClick={
                  closeSellDialog
                }
                className="bg-gray-300 px-4 py-2 rounded"
              >
                Cancel
              </button>


              <button
                type="button"
                onClick={handleSell}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
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