import { useState } from "react";

function PortfolioBuilder({ onAdd, onSell }) {

  const [mode, setMode] = useState("buy");

  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");

  function handleSubmit(e) {

    e.preventDefault();

    if (!symbol || !quantity || !price) {
      return;
    }

    if (mode === "buy") {

      onAdd({

        symbol: symbol.toUpperCase(),

        quantity: Number(quantity),

        buyPrice: Number(price)

      });

    } else {

      onSell({

        symbol: symbol.toUpperCase(),

        quantity: Number(quantity),

        sellPrice: Number(price)

      });

    }

    setSymbol("");
    setQuantity("");
    setPrice("");
  }

  return (

    <div className="bg-white p-6 rounded shadow">

      <h2 className="text-xl font-bold mb-4">
        💼 Portfolio Builder
      </h2>

      {/* ======================================================
          MODE BUTTONS
      ====================================================== */}

      <div className="flex gap-3 mb-4">

        <button
          type="button"
          onClick={() => setMode("buy")}
          className={`px-5 py-2 rounded ${
            mode === "buy"
              ? "bg-blue-600 text-white"
              : "bg-gray-200"
          }`}
        >
          Buy / Add
        </button>

        <button
          type="button"
          onClick={() => setMode("sell")}
          className={`px-5 py-2 rounded ${
            mode === "sell"
              ? "bg-red-600 text-white"
              : "bg-gray-200"
          }`}
        >
          Sell / Remove
        </button>

      </div>

      {/* ======================================================
          FORM
      ====================================================== */}

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-4 gap-3"
      >

        <input
          className="border p-2 rounded"
          placeholder="Symbol"
          value={symbol}
          onChange={(e) =>
            setSymbol(
              e.target.value.toUpperCase()
            )
          }
        />

        <input
          className="border p-2 rounded"
          type="number"
          min="1"
          placeholder={
            mode === "buy"
              ? "Quantity"
              : "Sell Quantity"
          }
          value={quantity}
          onChange={(e) =>
            setQuantity(e.target.value)
          }
        />

        <input
          className="border p-2 rounded"
          type="number"
          min="0"
          step="0.01"
          placeholder={
            mode === "buy"
              ? "Buy Price"
              : "Sell Price"
          }
          value={price}
          onChange={(e) =>
            setPrice(e.target.value)
          }
        />

        <button
          className={`text-white rounded ${
            mode === "buy"
              ? "bg-blue-600"
              : "bg-red-600"
          }`}
          type="submit"
        >
          {mode === "buy"
            ? "Add"
            : "Sell"}
        </button>

      </form>

    </div>
  );
}

export default PortfolioBuilder;