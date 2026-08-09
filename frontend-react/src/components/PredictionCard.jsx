function PredictionCard({ prediction }) {
  if (!prediction) return null;

  const currentPrice = Number(prediction.currentPrice) || 0;
  const predictedPrice = Number(prediction.predictedPrice) || 0;

  const priceChange = predictedPrice - currentPrice;

  const percentageChange =
    currentPrice !== 0
      ? (priceChange / currentPrice) * 100
      : 0;

  const isBullish = prediction.trend === "Bullish";

  const ma20 = Number(prediction.signals?.ma20);
  const ma50 = Number(prediction.signals?.ma50);
  const momentum20 = Number(prediction.signals?.momentum20);
  const rsi = Number(prediction.signals?.rsi);
  const volatility = Number(prediction.signals?.volatility);

  return (
    <div className="bg-white rounded-xl shadow p-6">

      <h2 className="text-2xl font-bold mb-6">
        🔮 AI Stock Prediction
      </h2>

      {/* Main Prediction */}
      <div className="grid md:grid-cols-2 gap-4">

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Current Price
          </p>

          <p className="text-2xl font-bold">
            ₹{currentPrice.toFixed(2)}
          </p>
        </div>

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Predicted Price
          </p>

          <p className="text-2xl font-bold">
            ₹{predictedPrice.toFixed(2)}
          </p>
        </div>

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Expected Change
          </p>

          <p className="text-xl font-bold">
            ₹{priceChange.toFixed(2)}
          </p>

          <p>
            {percentageChange.toFixed(2)}%
          </p>
        </div>

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Trend
          </p>

          <p className="text-xl font-bold">
            {isBullish ? "📈 Bullish" : "📉 Bearish"}
          </p>
        </div>

      </div>

      {/* Recommendation */}
      <div className="mt-6">

        <p>
          <strong>Confidence:</strong>{" "}
          {prediction.confidence}%
        </p>

        <p className="mt-2">
          <strong>Recommendation:</strong>{" "}
          {prediction.recommendation}
        </p>

      </div>

      {/* Technical Signals */}
      <div className="mt-8">

        <h3 className="text-xl font-bold mb-4">
          📊 Technical Signals
        </h3>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">

          <div className="border rounded-lg p-3">
            <p className="text-gray-500">
              MA20
            </p>

            <p className="font-bold">
              {Number.isFinite(ma20)
                ? `₹${ma20.toFixed(2)}`
                : "N/A"}
            </p>
          </div>

          <div className="border rounded-lg p-3">
            <p className="text-gray-500">
              MA50
            </p>

            <p className="font-bold">
              {Number.isFinite(ma50)
                ? `₹${ma50.toFixed(2)}`
                : "N/A"}
            </p>
          </div>

          <div className="border rounded-lg p-3">
            <p className="text-gray-500">
              20-Day Momentum
            </p>

            <p className="font-bold">
              {Number.isFinite(momentum20)
                ? `${momentum20.toFixed(2)}%`
                : "N/A"}
            </p>
          </div>

          <div className="border rounded-lg p-3">
            <p className="text-gray-500">
              RSI
            </p>

            <p className="font-bold">
              {Number.isFinite(rsi)
                ? rsi.toFixed(2)
                : "N/A"}
            </p>
          </div>

          <div className="border rounded-lg p-3">
            <p className="text-gray-500">
              Volatility
            </p>

            <p className="font-bold">
              {Number.isFinite(volatility)
                ? `${volatility.toFixed(2)}%`
                : "N/A"}
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default PredictionCard;