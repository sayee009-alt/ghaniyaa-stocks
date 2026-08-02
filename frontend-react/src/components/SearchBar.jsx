import { useState } from "react";

function SearchBar({ onAnalyze }) {
  const [symbol, setSymbol] = useState("");

  return (
    <div style={{ margin: "20px 0" }}>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Enter Stock Symbol"
      />

      <button
        style={{ marginLeft: "10px" }}
        onClick={() => onAnalyze(symbol)}
      >
        Analyze
      </button>
    </div>
  );
}

export default SearchBar;