function DecisionCard({ decision }) {

  if (!decision) return null;

  const recommendation = decision.recommendation;

  let badgeClass =
    "bg-gray-100 text-gray-800";

  if (recommendation === "BUY") {
    badgeClass =
      "bg-green-100 text-green-700";
  }

  if (recommendation === "SELL") {
    badgeClass =
      "bg-red-100 text-red-700";
  }

  if (recommendation === "HOLD") {
    badgeClass =
      "bg-yellow-100 text-yellow-700";
  }

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-8">

      <h2 className="text-2xl font-bold mb-5">
        🧠 Ghaniyaa Decision Engine
      </h2>

      <div className="grid md:grid-cols-3 gap-4">

        <div className="border rounded-lg p-4">

          <p className="text-gray-500">
            Fundamental Score
          </p>

          <p className="text-2xl font-bold">
            {decision.fundamentalScore}/100
          </p>

        </div>

        <div className="border rounded-lg p-4">

          <p className="text-gray-500">
            Technical Score
          </p>

          <p className="text-2xl font-bold">
            {decision.technicalScore}/100
          </p>

        </div>

        <div className="border rounded-lg p-4">

          <p className="text-gray-500">
            Final Ghaniyaa Score
          </p>

          <p className="text-2xl font-bold">
            {decision.finalScore}/100
          </p>

        </div>

      </div>

      <div className="mt-6">

        <span
          className={`inline-block px-5 py-2 rounded-full font-bold ${badgeClass}`}
        >
          {recommendation}
        </span>

      </div>

      <div className="mt-4">

        <p>
          <strong>Confidence:</strong>{" "}
          {decision.confidence}%
        </p>

      </div>

      <div className="mt-6">

        <h3 className="font-bold mb-3">
          Technical Signals
        </h3>

        <div className="grid md:grid-cols-4 gap-3">

          <div className="border rounded p-3">
            <p className="text-gray-500">
              MA20
            </p>

            <p className="font-bold">
              ₹{decision.signals?.ma20}
            </p>
          </div>

          <div className="border rounded p-3">
            <p className="text-gray-500">
              MA50
            </p>

            <p className="font-bold">
              ₹{decision.signals?.ma50}
            </p>
          </div>

          <div className="border rounded p-3">
            <p className="text-gray-500">
              Momentum
            </p>

            <p className="font-bold">
              {decision.signals?.momentum}%
            </p>
          </div>

          <div className="border rounded p-3">
            <p className="text-gray-500">
              RSI
            </p>

            <p className="font-bold">
              {decision.signals?.rsi}
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default DecisionCard;