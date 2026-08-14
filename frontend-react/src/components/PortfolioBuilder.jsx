import { useState } from "react";

function PortfolioBuilder({ onAdd }) {

  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");

  const [symbolStatus, setSymbolStatus] = useState("");
  const [validSymbol, setValidSymbol] = useState(false);

  function validateSymbol(value) {

    const cleanedSymbol = value
      .trim()
      .toUpperCase();

    setSymbol(cleanedSymbol);

    setQuantity("");
    setPrice("");

    if (!cleanedSymbol) {

      setSymbolStatus("");
      setValidSymbol(false);

      return;
    }

    /*
     * Basic stock-symbol format validation.
     *
     * Real stock validation is still performed
     * by the backend before saving.
     */

    const symbolPattern = /^[A-Z][A-Z0-9&.-]{1,19}$/;

    if (!symbolPattern.test(cleanedSymbol)) {

      setSymbolStatus(
        "❌ Invalid stock symbol format"
      );

      setValidSymbol(false);

      return;
    }

    setSymbolStatus(
      "✓ Symbol format looks valid"
    );

    setValidSymbol(true);
  }

  function handleSubmit(e) {

    e.preventDefault();

    if (!validSymbol) {

      alert(
        "Please enter a valid stock symbol."
      );

      return;
    }

    if (!quantity || Number(quantity) <= 0) {

      alert(
        "Please enter a valid quantity."
      );

      return;
    }

    if (!price || Number(price) <= 0) {

      alert(
        "Please enter a valid buy price."
      );

      return;
    }

    onAdd({

      symbol: symbol.toUpperCase(),

      quantity: Number(quantity),

      buyPrice: Number(price)

    });

    setSymbol("");
    setQuantity("");
    setPrice("");

    setSymbolStatus("");
    setValidSymbol(false);
  }

  return (

    <div className="bg-white p-6 rounded shadow">

      <h2 className="text-xl font-bold mb-4">
        💼 Add to Portfolio
      </h2>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-4 gap-3"
      >

        {/* =====================================================
            SYMBOL
        ====================================================== */}

        <div>

          <input
            className="border p-2 rounded w-full"
            placeholder="Symbol"
            value={symbol}
            maxLength={20}
            onChange={(e) => {

              const value = e.target.value
                .toUpperCase()
                .replace(/[^A-Z0-9&.-]/g, "");

              validateSymbol(value);

            }}
          />

          {symbolStatus && (

            <p
              className={`text-sm mt-1 ${
                validSymbol
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {symbolStatus}
            </p>

          )}

        </div>


        {/* =====================================================
            QUANTITY
        ====================================================== */}

        <input
          className="border p-2 rounded"
          type="number"
          min="1"
          step="1"
          placeholder="Quantity"
          value={quantity}
          disabled={!validSymbol}
          onChange={(e) => {

            const value = e.target.value;

            if (
              value === "" ||
              /^\d+$/.test(value)
            ) {

              setQuantity(value);

            }

          }}
        />


        {/* =====================================================
            BUY PRICE
        ====================================================== */}

        <input
          className="border p-2 rounded"
          type="number"
          min="0.01"
          step="0.01"
          placeholder="Buy Price"
          value={price}
          disabled={!validSymbol}
          onChange={(e) =>
            setPrice(e.target.value)
          }
        />


        {/* =====================================================
            ADD BUTTON
        ====================================================== */}

        <button
          className="bg-blue-600 text-white rounded px-4 py-2 disabled:bg-gray-400"
          type="submit"
          disabled={
            !validSymbol ||
            !quantity ||
            !price
          }
        >
          Add to Portfolio
        </button>

      </form>

    </div>

  );
}

export default PortfolioBuilder;