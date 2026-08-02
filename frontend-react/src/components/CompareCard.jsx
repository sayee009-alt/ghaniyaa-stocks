function CompareCard({ comparison }) {
  if (!comparison) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        Stock comparison will appear here.
      </div>
    );
  }

  const { stock1, stock2 } = comparison;

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-bold mb-6">
        ⚖️ Stock Comparison
      </h2>

      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b">
            <th className="text-left p-2">Metric</th>
            <th className="text-left p-2">{stock1.symbol}</th>
            <th className="text-left p-2">{stock2.symbol}</th>
          </tr>
        </thead>

        <tbody>
          <tr className="border-b">
            <td className="p-2">Price</td>
            <td className="p-2">₹{stock1.price}</td>
            <td className="p-2">₹{stock2.price}</td>
          </tr>

          <tr className="border-b">
            <td className="p-2">P/E</td>
            <td className="p-2">{stock1.pe}</td>
            <td className="p-2">{stock2.pe}</td>
          </tr>

          <tr>
            <td className="p-2">ROE</td>
            <td className="p-2">{stock1.roe}</td>
            <td className="p-2">{stock2.roe}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default CompareCard;