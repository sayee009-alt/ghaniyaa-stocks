function PortfolioCard({ portfolio }) {
  if (!portfolio) {
    return (
      <div className="bg-white p-6 rounded shadow">
        Portfolio is empty.
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-4">
        💼 Portfolio Dashboard
      </h2>
<h2>Total Investment</h2>
<p>₹{portfolio.totalInvestment}</p>

<h2>Current Value</h2>
<p>₹{portfolio.currentValue}</p>

<h2>Total Profit</h2>
<p className="text-green-600">
₹{portfolio.profit}
</p>
      <div className="grid grid-cols-3 gap-4 mb-6">

        <div className="bg-blue-50 p-4 rounded">
          <h3 className="font-semibold">Investment</h3>
          <p className="text-xl font-bold">
            ₹{portfolio.totalInvestment.toFixed(2)}
          </p>
        </div>

        <div className="bg-green-50 p-4 rounded">
          <h3 className="font-semibold">Current Value</h3>
          <p className="text-xl font-bold">
            ₹{portfolio.currentValue.toFixed(2)}
          </p>
        </div>

        <div className="bg-yellow-50 p-4 rounded">
          <h3 className="font-semibold">Profit / Loss</h3>
          <p
            className={`text-xl font-bold ${
              portfolio.profit >= 0
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            ₹{portfolio.profit.toFixed(2)}
          </p>
        </div>

      </div>

      <table className="w-full border">

        <thead className="bg-gray-100">

          <tr>
            <th className="border p-2">Symbol</th>
            <th className="border p-2">Qty</th>
            <th className="border p-2">Buy</th>
            <th className="border p-2">Current</th>
            <th className="border p-2">Investment</th>
            <th className="border p-2">Value</th>
            <th className="border p-2">Profit</th>
          </tr>

        </thead>

        <tbody>

          {portfolio.holdings.map((stock) => (

            <tr key={stock.symbol}>

              <td className="border p-2">{stock.symbol}</td>

              <td className="border p-2">{stock.quantity}</td>

              <td className="border p-2">
                ₹{stock.buyPrice}
              </td>

              <td className="border p-2">
                ₹{stock.currentPrice}
              </td>

              <td className="border p-2">
                ₹{stock.investment.toFixed(2)}
              </td>

              <td className="border p-2">
                ₹{stock.currentValue.toFixed(2)}
              </td>

              <td
                className={`border p-2 ${
                  stock.profit >= 0
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                ₹{stock.profit.toFixed(2)}
              </td>

            </tr>

          ))}

        </tbody>

      </table>
    </div>
  );
}

export default PortfolioCard;