import { useEffect, useState } from "react";
import { getScreener } from "../services/api";

function Screener() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    async function loadStocks() {
      const data = await getScreener();
      setStocks(data);
    }

    loadStocks();
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-8">

      <h1 className="text-3xl font-bold mb-6">
        📊 Ghaniyaa Stock Screener
      </h1>

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

export default Screener;