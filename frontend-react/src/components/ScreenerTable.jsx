function ScreenerTable({ stocks }) {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-2xl font-bold mb-4">
        📊 Stock Screener
      </h2>

      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2">Symbol</th>
            <th className="p-2">Company</th>
            <th className="p-2">Price</th>
            <th className="p-2">Sector</th>
            <th className="p-2">Score</th>
          </tr>
        </thead>

        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.symbol} className="border-b">
              <td className="p-2">{stock.symbol}</td>
              <td className="p-2">{stock.company}</td>
              <td className="p-2">₹{stock.price}</td>
              <td className="p-2">{stock.sector}</td>
              <td className="p-2 font-bold text-green-600">
                {stock.score}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ScreenerTable;