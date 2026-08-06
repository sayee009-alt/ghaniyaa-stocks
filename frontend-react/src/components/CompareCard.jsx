function CompareCard({ comparison }) {
  if (!comparison) {
    return (
      <div className="bg-white p-6 rounded shadow">
        Compare two stocks to see their metrics.
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">
        📊 Stock Comparison
      </h2>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Metric</th>
            <th className="border p-2">{comparison.stock1.symbol}</th>
            <th className="border p-2">{comparison.stock2.symbol}</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td className="border p-2">Company</td>
            <td className="border p-2">{comparison.stock1.company}</td>
            <td className="border p-2">{comparison.stock2.company}</td>
          </tr>

          <tr>
            <td className="border p-2">Price</td>
            <td className="border p-2">₹{comparison.stock1.price}</td>
            <td className="border p-2">₹{comparison.stock2.price}</td>
          </tr>

          <tr>
            <td className="border p-2">P/E</td>
            <td className="border p-2">{comparison.stock1.pe}</td>
            <td className="border p-2">{comparison.stock2.pe}</td>
          </tr>

          <tr>
            <td className="border p-2">ROE</td>
            <td className="border p-2">{comparison.stock1.roe}</td>
            <td className="border p-2">{comparison.stock2.roe}</td>
          </tr>
        </tbody>
      </table>
      <div className="mt-6 p-4 bg-green-100 rounded">
  <h3 className="text-lg font-bold">
    🏆 Ghaniyaa AI Verdict
  </h3>

  <p className="mt-2">
    Winner:
    <span className="font-bold text-green-700">
      {" "}
      {comparison.winner}
    </span>
  </p>

  <p className="text-gray-700 mt-2">
    {comparison.reason}
  </p>
</div>
    </div>
      );
}

export default CompareCard;