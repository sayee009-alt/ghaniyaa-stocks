function ThesisCard({ thesis }) {

  if (!thesis) return null;

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-8">

      <h2 className="text-2xl font-bold mb-5">
        🧠 Ghaniyaa Investment Thesis
      </h2>

      <div className="grid md:grid-cols-3 gap-4">

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Fundamental
          </p>

          <p className="text-2xl font-bold">
            {thesis.fundamentalScore}/100
          </p>
        </div>

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Technical
          </p>

          <p className="text-2xl font-bold">
            {thesis.technicalScore}/100
          </p>
        </div>

        <div className="border rounded-lg p-4">
          <p className="text-gray-500">
            Final Score
          </p>

          <p className="text-2xl font-bold">
            {thesis.finalScore}/100
          </p>
        </div>

      </div>

      <div className="mt-6">

        <span className="inline-block bg-green-100 text-green-700 px-5 py-2 rounded-full font-bold">
          {thesis.recommendation}
        </span>

      </div>

      <div className="mt-6">

        <h3 className="text-lg font-bold mb-3">
          ✅ Why Ghaniyaa Likes This Stock
        </h3>

        <ul className="space-y-2">

          {thesis.positives?.map(
            (item, index) => (
              <li key={index}>
                ✓ {item}
              </li>
            )
          )}

        </ul>

      </div>

      <div className="mt-6">

        <h3 className="text-lg font-bold mb-3">
          ⚠ Risk Factors
        </h3>

        <ul className="space-y-2">

          {thesis.risks?.map(
            (item, index) => (
              <li key={index}>
                ⚠ {item}
              </li>
            )
          )}

        </ul>

      </div>

      <div className="mt-6">

        <h3 className="text-lg font-bold">
          Overall View
        </h3>

        <p className="text-lg mt-2">
          {thesis.overallView}
        </p>

      </div>

    </div>
  );
}

export default ThesisCard;