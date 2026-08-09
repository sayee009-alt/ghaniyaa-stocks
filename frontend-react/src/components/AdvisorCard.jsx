import { useEffect, useState } from "react";
import { getAdvisor } from "../services/api";

export default function AdvisorCard() {
  const [advisor, setAdvisor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadAdvisor() {
      try {
        setLoading(true);
        setError(null);

        const data = await getAdvisor();

        console.log("Advisor API:", data);

        setAdvisor(data);
      } catch (error) {
        console.error("Advisor Error:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadAdvisor();
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">
          🤖 AI Portfolio Advisor
        </h2>

        <p className="text-gray-500">
          Loading AI Advisor...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">
          🤖 AI Portfolio Advisor
        </h2>

        <p className="text-red-600">
          Failed to load AI Advisor.
        </p>

        <p className="text-sm text-gray-500 mt-2">
          {error}
        </p>
      </div>
    );
  }

  if (!advisor) {
    return null;
  }

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-6">

      <h2 className="text-xl font-bold mb-4">
        🤖 AI Portfolio Advisor
      </h2>

      <p>
        <strong>Health Score:</strong>{" "}
        {advisor.health_score}/100
      </p>

      <p>
        <strong>Risk:</strong>{" "}
        {advisor.risk}
      </p>

      <p>
        <strong>Diversification:</strong>{" "}
        {advisor.diversification}
      </p>

      <p className="mt-3">
        {advisor.recommendation}
      </p>

    </div>
  );
}