function StockCard({ stock, score }) {
  if (!stock) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        Search for a stock to view details.
      </div>
    );
  }

  const rating = score
    ? score.ghaniyaa_score >= 90
      ? "Excellent"
      : score.ghaniyaa_score >= 75
      ? "Good"
      : score.ghaniyaa_score >= 60
      ? "Average"
      : "Risky"
    : "";

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">

      {/* Ghaniyaa Score */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">⭐ Ghaniyaa Score</h3>

        <p className="text-4xl font-bold mt-2">
          {score ? score.ghaniyaa_score : "--"}
        </p>

        <p className="text-green-600 font-semibold">
          {rating}
        </p>
      </div>

      {/* Current Price */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">💰 Current Price</h3>

        <p className="text-2xl font-bold mt-2">
          ₹ {stock.price}
        </p>
      </div>

      {/* Company */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">🏢 Company</h3>

        <p className="font-semibold mt-2">
          {stock.company}
        </p>
      </div>

      {/* Sector */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">🏭 Sector</h3>

        <p className="mt-2">
          {stock.sector}
        </p>
      </div>

      {/* Market Cap */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-gray-500">📊 Market Cap</h3>

        <p className="mt-2">
          {stock.marketCap}
        </p>
      </div>

    </div>
  );
}

export default StockCard;