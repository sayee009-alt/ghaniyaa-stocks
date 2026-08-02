function FinancialCard({ financials }) {
  if (!financials) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        Financial information will appear here.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">

      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">📊 P/E Ratio</h3>
        <p className="text-xl font-bold mt-2">
          {financials.pe_ratio ?? "N/A"}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">📈 ROE</h3>
        <p className="text-xl font-bold mt-2">
          {financials.roe ?? "N/A"}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">🏦 Debt / Equity</h3>
        <p className="text-xl font-bold mt-2">
          {financials.debt_to_equity ?? "N/A"}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">💵 Dividend Yield</h3>
        <p className="text-xl font-bold mt-2">
          {financials.dividend_yield ?? "N/A"}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">💰 Market Cap</h3>
        <p className="text-xl font-bold mt-2">
          {financials.market_cap ?? "N/A"}
        </p>
      </div>

    </div>
  );
}

export default FinancialCard;