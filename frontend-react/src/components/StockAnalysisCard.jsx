function StockAnalysisCard({ analysis, loading, onClose }) {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p className="text-gray-500">
          Loading stock analysis...
        </p>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  if (!analysis.success) {
    return (
      <div className="bg-white p-6 rounded shadow">

        <div className="flex justify-between items-center mb-4">

          <h2 className="text-xl font-bold">
            Stock Analysis
          </h2>

          {onClose && (
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-black"
            >
              ✕
            </button>
          )}

        </div>

        <p className="text-red-600">
          {analysis.error || "Unable to load stock analysis."}
        </p>

      </div>
    );
  }

  const formatNumber = (value, digits = 2) => {
    if (value === null || value === undefined) {
      return "-";
    }

    return Number(value).toLocaleString("en-IN", {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits,
    });
  };

  const formatPercent = (value) => {
    if (value === null || value === undefined) {
      return "-";
    }

    return `${(Number(value) * 100).toFixed(2)}%`;
  };

  const formatDividend = (value) => {
    if (value === null || value === undefined) {
      return "-";
    }

    return `${Number(value).toFixed(2)}%`;
  };

  const score = Number(analysis.score ?? 0);

  let scoreClass = "text-red-600";

  if (score >= 80) {
    scoreClass = "text-green-600";
  } else if (score >= 60) {
    scoreClass = "text-yellow-600";
  }

  return (
    <div className="bg-white p-6 rounded shadow">

      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="flex justify-between items-start mb-6">

        <div>

          <div className="flex items-center gap-3">

            <h2 className="text-2xl font-bold">
              {analysis.symbol}
            </h2>

            <span
              className={`text-2xl font-bold ${scoreClass}`}
            >
              {analysis.score ?? "-"}
            </span>

          </div>

          <p className="text-gray-600">
            {analysis.company}
          </p>

          <p className="text-sm text-gray-500 mt-1">
            {analysis.sector}
          </p>

        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-black text-xl"
          >
            ✕
          </button>
        )}

      </div>


      {/* ================================================== */}
      {/* PRICE */}
      {/* ================================================== */}

      <div className="mb-6">

        <p className="text-sm text-gray-500">
          Current Price
        </p>

        <p className="text-3xl font-bold">
          ₹{formatNumber(analysis.price)}
        </p>

      </div>


      {/* ================================================== */}
      {/* KEY METRICS */}
      {/* ================================================== */}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

        {/* P/E */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            P/E
          </p>

          <p className="text-xl font-bold">
            {formatNumber(analysis.pe)}
          </p>

        </div>


        {/* Forward P/E */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Forward P/E
          </p>

          <p className="text-xl font-bold">
            {formatNumber(analysis.forwardPE)}
          </p>

        </div>


        {/* ROE */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            ROE
          </p>

          <p className="text-xl font-bold">
            {formatPercent(analysis.roe)}
          </p>

        </div>


        {/* Profit Margin */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Profit Margin
          </p>

          <p className="text-xl font-bold">
            {formatPercent(analysis.profitMargin)}
          </p>

        </div>


        {/* Revenue Growth */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Revenue Growth
          </p>

          <p className="text-xl font-bold">
            {formatPercent(analysis.revenueGrowth)}
          </p>

        </div>


        {/* Earnings Growth */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Earnings Growth
          </p>

          <p className="text-xl font-bold">
            {formatPercent(analysis.earningsGrowth)}
          </p>

        </div>


        {/* Dividend Yield */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Dividend Yield
          </p>

          <p className="text-xl font-bold">
            {formatDividend(analysis.dividendYield)}
          </p>

        </div>


        {/* Market Cap */}

        <div className="border rounded p-4">

          <p className="text-sm text-gray-500">
            Market Cap
          </p>

          <p className="text-xl font-bold">
            {analysis.marketCap
              ? `₹${formatNumber(
                  analysis.marketCap / 10000000,
                  2
                )} Cr`
              : "-"}

          </p>

        </div>

      </div>


      {/* ================================================== */}
      {/* 52 WEEK RANGE */}
      {/* ================================================== */}

      <div className="mt-6 border rounded p-4">

        <h3 className="font-bold mb-3">
          52-Week Range
        </h3>

        <div className="flex justify-between">

          <div>

            <p className="text-sm text-gray-500">
              Low
            </p>

            <p className="font-bold">
              ₹{formatNumber(analysis["52WeekLow"])}
            </p>

          </div>

          <div className="text-right">

            <p className="text-sm text-gray-500">
              High
            </p>

            <p className="font-bold">
              ₹{formatNumber(analysis["52WeekHigh"])}
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default StockAnalysisCard;