import { useState } from "react";

function PortfolioBuilder({ onAdd }) {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");
  const [buyPrice, setBuyPrice] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!symbol || !quantity || !buyPrice) return;

    onAdd({
      symbol: symbol.toUpperCase(),
      quantity: Number(quantity),
      buyPrice: Number(buyPrice),
    });

    setSymbol("");
    setQuantity("");
    setBuyPrice("");
  }

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">
        💼 Portfolio Builder
      </h2>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-4 gap-3"
      >
        <input
          className="border p-2 rounded"
          placeholder="Symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Buy Price"
          value={buyPrice}
          onChange={(e) => setBuyPrice(e.target.value)}
        />

        <button
          className="bg-blue-600 text-white rounded"
          type="submit"
        >
          Add
        </button>
      </form>
    </div>
  );
}

export default PortfolioBuilder;