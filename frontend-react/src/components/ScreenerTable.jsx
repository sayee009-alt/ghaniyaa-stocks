function ScreenerTable({ stocks, onSelectStock }) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">
        📊 Stock Screener
      </h2>

      {!stocks || stocks.length === 0 ? (
        <p className="text-gray-500">
          No stocks available.
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">

            <thead className="bg-gray-200">
              <tr>
                <th className="p-3 text-left border">
                  Rank
                </th>

                <th className="p-3 text-left border">
                  Symbol
                </th>

                <th className="p-3 text-left border">
                  Company
                </th>

                <th className="p-3 text-right border">
                  Price
                </th>

                <th className="p-3 text-left border">
                  Sector
                </th>

                <th className="p-3 text-right border">
                  Score
                </th>
              </tr>
            </thead>

            <tbody>
              {stocks.map((stock) => (
                <tr
                  key={stock.symbol}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-3 border">
                    {stock.rank ?? "-"}
                  </td>

                  <td className="p-3 border">
                    <button
                      onClick={() =>
                        onSelectStock(stock.symbol)
                      }
                      className="font-bold text-blue-600 hover:underline"
                    >
                      {stock.symbol}
                    </button>
                  </td>

                  <td className="p-3 border">
                    {stock.company}
                  </td>

                  <td className="p-3 border text-right">
                    {stock.price != null
                      ? `₹${Number(stock.price).toLocaleString(
                          "en-IN",
                          {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          }
                        )}`
                      : "-"}
                  </td>

                  <td className="p-3 border">
                    {stock.sector || "-"}
                  </td>

                  <td className="p-3 border text-right">
                    <span
                      className={
                        stock.score >= 80
                          ? "font-bold text-green-600"
                          : stock.score >= 60
                          ? "font-bold text-yellow-600"
                          : "font-bold text-red-600"
                      }
                    >
                      {stock.score ?? "-"}
                    </span>
                  </td>

                </tr>
              ))}
            </tbody>

          </table>
        </div>
      )}
    </div>
  );
}

export default ScreenerTable;