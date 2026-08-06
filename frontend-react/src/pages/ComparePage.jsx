import { useState } from "react";
import { compareStocks } from "../services/api";

function ComparePage() {
  const [symbol1, setSymbol1] = useState("");
  const [symbol2, setSymbol2] = useState("");
  const [result, setResult] = useState(null);

  async function handleCompare() {
    if (!symbol1 || !symbol2) return;

    try {
      const data = await compareStocks(symbol1, symbol2);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Comparison failed");
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-8">

      <h1 className="text-3xl font-bold mb-6">
        📊 Compare Stocks
      </h1>

      <div className="flex gap-4 mb-6">

        <input
          value={symbol1}
          onChange={(e) => setSymbol1(e.target.value)}
          placeholder="First Stock"
          className="border p-2 rounded w-full"
        />

        <input
          value={symbol2}
          onChange={(e) => setSymbol2(e.target.value)}
          placeholder="Second Stock"
          className="border p-2 rounded w-full"
        />

        <button
          onClick={handleCompare}
          className="bg-blue-600 text-white px-6 rounded"
        >
          Compare
        </button>

      </div>

      {result && (
        <div className="grid grid-cols-2 gap-6">

          <div className="border rounded p-4">

            <h2 className="font-bold text-xl">
              {result.stock1.company}
            </h2>

            <p>Price: ₹{result.stock1.price}</p>
            <p>PE: {result.stock1.pe}</p>
            <p>ROE: {result.stock1.roe}</p>

          </div>

          <div className="border rounded p-4">

            <h2 className="font-bold text-xl">
              {result.stock2.company}
            </h2>

            <p>Price: ₹{result.stock2.price}</p>
            <p>PE: {result.stock2.pe}</p>
            <p>ROE: {result.stock2.roe}</p>

          </div>

        </div>
      )}

    </div>
  );
}

export default ComparePage;