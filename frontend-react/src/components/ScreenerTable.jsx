function ScreenerTable({ stocks }) {

  // ==========================================================
  // Normalize Screener API response
  // ==========================================================
  //
  // New API response:
  //
  // {
  //   stocks: [...],
  //   count: 17,
  //   invalidCount: 1,
  //   invalid: [...]
  // }
  //
  // Older response:
  //
  // [...]
  //
  // This component supports both.
  // ==========================================================

  const stockList = Array.isArray(stocks)
    ? stocks
    : stocks?.stocks || [];

  const invalidStocks = Array.isArray(stocks?.invalid)
    ? stocks.invalid
    : [];


  return (

    <div className="bg-white p-6 rounded shadow">

      {/* =====================================================
          HEADER
          ===================================================== */}

      <div className="flex items-center justify-between mb-5">

        <h2 className="text-2xl font-bold">
          📊 Stock Screener
        </h2>

        <div className="text-sm text-gray-500">

          {stockList.length} valid stocks

        </div>

      </div>


      {/* =====================================================
          EMPTY STATE
          ===================================================== */}

      {stockList.length === 0 ? (

        <div className="border rounded-lg p-6 text-center text-gray-500">

          No screener data available.

        </div>

      ) : (

        <div className="overflow-x-auto">

          <table className="w-full border">

            <thead className="bg-gray-200">

              <tr>

                <th className="p-2 text-left">
                  Symbol
                </th>

                <th className="p-2 text-left">
                  Company
                </th>

                <th className="p-2 text-left">
                  Price
                </th>

                <th className="p-2 text-left">
                  Sector
                </th>

                <th className="p-2 text-left">
                  Score
                </th>

              </tr>

            </thead>


            <tbody>

              {stockList.map((stock) => (

                <tr
                  key={stock.symbol}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-2 font-semibold">
                    {stock.symbol}
                  </td>


                  <td className="p-2">
                    {stock.company || "Unknown"}
                  </td>


                  <td className="p-2">

                    {stock.price !== null &&
                    stock.price !== undefined
                      ? `₹${Number(stock.price).toLocaleString("en-IN", {
                          maximumFractionDigits: 2,
                        })}`
                      : "N/A"}

                  </td>


                  <td className="p-2">
                    {stock.sector || "Unknown"}
                  </td>


                  <td className="p-2">

                    <span className="font-bold text-green-600">
                      {stock.score ?? "N/A"}
                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      )}


      {/* =====================================================
          INVALID STOCKS
          ===================================================== */}

      {invalidStocks.length > 0 && (

        <div className="mt-6">

          <h3 className="font-bold text-gray-700 mb-3">

            ⚠️ Market Data Unavailable

          </h3>


          <div className="space-y-2">

            {invalidStocks.map((stock) => (

              <div
                key={stock.symbol}
                className="border rounded-lg p-3 bg-yellow-50"
              >

                <div className="font-semibold">
                  {stock.symbol}
                </div>

                <div className="text-sm text-gray-600">
                  {stock.reason || "Market data unavailable"}
                </div>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>

  );
}


export default ScreenerTable;