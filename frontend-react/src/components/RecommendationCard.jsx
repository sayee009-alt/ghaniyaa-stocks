function RecommendationCard({ score }) {
  if (!score) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        AI Recommendation will appear here.
      </div>
    );
  }

  let recommendation = "";
  let color = "";
  let confidence = "";

  if (score.ghaniyaa_score >= 90) {
    recommendation = "🟢 Strong Buy";
    color = "text-green-600";
    confidence = "High";
  } else if (score.ghaniyaa_score >= 75) {
    recommendation = "🔵 Buy";
    color = "text-blue-600";
    confidence = "Good";
  } else if (score.ghaniyaa_score >= 60) {
    recommendation = "🟡 Hold";
    color = "text-yellow-500";
    confidence = "Medium";
  } else {
    recommendation = "🔴 Avoid";
    color = "text-red-600";
    confidence = "Low";
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold">
        📈 AI Recommendation
      </h2>

      <p className={`text-3xl font-bold mt-4 ${color}`}>
        {recommendation}
      </p>

      <p className="mt-3">
        Confidence: <strong>{confidence}</strong>
      </p>
    </div>
  );
}

export default RecommendationCard;