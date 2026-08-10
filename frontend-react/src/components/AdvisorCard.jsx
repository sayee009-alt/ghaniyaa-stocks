import { useEffect, useState } from "react";
import { getAdvisor } from "../services/api";

import { Pie } from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

export default function AdvisorCard() {
  const [advisor, setAdvisor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --------------------------------
  // Load Advisor
  // --------------------------------

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

  // --------------------------------
  // Loading
  // --------------------------------

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

  // --------------------------------
  // Error
  // --------------------------------

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">
          🤖 AI Portfolio Advisor
        </h2>

        <p className="text-red-600 font-semibold">
          Failed to load AI Advisor.
        </p>

        <p className="text-sm text-gray-500 mt-2">
          {error}
        </p>
      </div>
    );
  }

  // --------------------------------
  // No Data
  // --------------------------------

  if (!advisor) {
    return null;
  }

  // --------------------------------
  // Safe Numeric Values
  // --------------------------------

  const healthScore = Number(
    advisor.health_score || 0
  );

  const portfolioRiskScore = Number(
    advisor.portfolio_risk_score || 0
  );

  const sectorScore = Number(
    advisor.sector_diversification_score || 0
  );

  const largestHoldingPercent = Number(
    advisor.largest_holding_percent || 0
  );

  const sectorCount = Number(
    advisor.sector_count || 0
  );

  const totalHoldings = Number(
    advisor.total_holdings || 0
  );

  const profitPercent = Number(
    advisor.profit_percent || 0
  );

  // --------------------------------
  // Portfolio Strength
  // --------------------------------
  //
  // IMPORTANT:
  // Risk Score is:
  // 0   = very high risk
  // 100 = low risk
  //
  // Therefore we use the risk score directly.
  // --------------------------------

  const portfolioStrength = Math.round(
    (
      healthScore +
      portfolioRiskScore +
      sectorScore
    ) / 3
  );

  let portfolioStrengthLabel = "Very Weak";

  if (portfolioStrength >= 80) {
    portfolioStrengthLabel = "Strong";
  } else if (portfolioStrength >= 60) {
    portfolioStrengthLabel = "Moderate";
  } else if (portfolioStrength >= 40) {
    portfolioStrengthLabel = "Weak";
  }

  // --------------------------------
  // Strength Color
  // --------------------------------

  let strengthColor = "bg-red-500";
  let strengthTextColor = "text-red-700";

  if (portfolioStrength >= 80) {
    strengthColor = "bg-green-500";
    strengthTextColor = "text-green-700";
  } else if (portfolioStrength >= 60) {
    strengthColor = "bg-yellow-500";
    strengthTextColor = "text-yellow-700";
  } else if (portfolioStrength >= 40) {
    strengthColor = "bg-orange-500";
    strengthTextColor = "text-orange-700";
  }

  // --------------------------------
  // Risk Gauge
  // --------------------------------

  let riskGaugeColor = "bg-red-500";

  if (portfolioRiskScore >= 80) {
    riskGaugeColor = "bg-green-500";
  } else if (portfolioRiskScore >= 60) {
    riskGaugeColor = "bg-yellow-500";
  } else if (portfolioRiskScore >= 40) {
    riskGaugeColor = "bg-orange-500";
  }

  const riskGaugeLabel =
    advisor.portfolio_risk || "Unknown Risk";

  // --------------------------------
  // Sector Data
  // --------------------------------

  const sectorLabels = Object.keys(
    advisor.sectors || {}
  );

  const sectorValues = Object.values(
    advisor.sectors || {}
  ).map((value) => Number(value));

  // --------------------------------
  // Largest Sector
  // --------------------------------

  const sectorEntries = Object.entries(
    advisor.sectors || {}
  );

  let largestSector = "Unknown";
  let largestSectorPercentage = 0;

  if (sectorEntries.length > 0) {
    const sortedSectors = [...sectorEntries].sort(
      (a, b) => Number(b[1]) - Number(a[1])
    );

    largestSector = sortedSectors[0][0];
    largestSectorPercentage = Number(
      sortedSectors[0][1]
    );
  }

  // --------------------------------
  // Pie Chart
  // --------------------------------

  const sectorChartData = {
    labels: sectorLabels,

    datasets: [
      {
        data: sectorValues,
        borderWidth: 1,
      },
    ],
  };

  const sectorChartOptions = {
    responsive: true,

    plugins: {
      legend: {
        position: "bottom",
      },
    },
  };

  // --------------------------------
  // Recommended Actions
  // --------------------------------

  const recommendedActions = [];

  // 1. Largest holding concentration

  if (largestHoldingPercent >= 70) {
    recommendedActions.push(
      `🚨 Very high concentration in ${advisor.largest_holding}. This holding represents ${largestHoldingPercent.toFixed(
        2
      )}% of your portfolio. Consider gradually reducing dependence on this single holding.`
    );
  } else if (largestHoldingPercent >= 50) {
    recommendedActions.push(
      `⚠️ ${advisor.largest_holding} represents ${largestHoldingPercent.toFixed(
        2
      )}% of your portfolio. Consider reducing concentration over time.`
    );
  } else if (largestHoldingPercent >= 30) {
    recommendedActions.push(
      `Monitor ${advisor.largest_holding} because it represents ${largestHoldingPercent.toFixed(
        2
      )}% of your portfolio.`
    );
  }

  // 2. Sector diversification

  if (sectorCount === 1) {
    recommendedActions.push(
      `🏭 Your portfolio is completely concentrated in ${largestSector}. Consider gradually adding quality companies from other sectors.`
    );
  } else if (sectorCount === 2) {
    recommendedActions.push(
      "🏭 Your portfolio spans only two sectors. Consider gradually adding exposure to additional sectors."
    );
  } else if (sectorCount < 4) {
    recommendedActions.push(
      "🏭 Consider increasing sector diversification to reduce dependence on a small number of industries."
    );
  }

  // 3. Number of holdings

  if (totalHoldings === 1) {
    recommendedActions.push(
      "📊 Your portfolio contains only one holding. Consider building a diversified portfolio gradually."
    );
  } else if (totalHoldings < 5) {
    recommendedActions.push(
      `📊 Your portfolio has only ${totalHoldings} holdings. Consider gradually adding other quality companies.`
    );
  }

  // 4. Negative performance

  if (profitPercent < 0) {
    recommendedActions.push(
      "📉 Your portfolio is currently below its total investment. Review individual holdings and their fundamentals before adding more capital."
    );
  }

  // 5. Very high portfolio risk

  if (advisor.portfolio_risk === "Very High") {
    recommendedActions.push(
      "🚨 Portfolio risk is very high. Prioritize diversification and position sizing before increasing exposure."
    );
  } else if (advisor.portfolio_risk === "High") {
    recommendedActions.push(
      "⚠️ Portfolio risk is high. Consider improving diversification and reducing excessive concentration."
    );
  }

  // 6. Healthy portfolio

  if (recommendedActions.length === 0) {
    recommendedActions.push(
      "✅ Your portfolio structure appears reasonably balanced. Continue monitoring diversification, risk and long-term performance."
    );
  }

  // --------------------------------
  // Main UI
  // --------------------------------

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-6">

      {/* -------------------------------- */}
      {/* Header */}
      {/* -------------------------------- */}

      <div className="flex items-center justify-between mb-6">

        <h2 className="text-2xl font-bold">
          🤖 AI Portfolio Advisor
        </h2>

        <span className="text-sm text-gray-500">
          AI Portfolio Analysis
        </span>

      </div>

      {/* -------------------------------- */}
      {/* Portfolio Strength */}
      {/* -------------------------------- */}

      <div className="border rounded-xl p-5 mb-6 bg-gray-50">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-gray-500">
              Overall Portfolio Strength
            </p>

            <p className="text-3xl font-bold mt-1">
              {portfolioStrength}/100
            </p>

          </div>

          <div className="text-right">

            <p className="text-sm text-gray-500">
              Rating
            </p>

            <p className="text-2xl font-bold">
              {portfolioStrengthLabel}
            </p>

          </div>

        </div>

        {/* Strength Bar */}

        <div className="w-full bg-gray-200 rounded-full h-4 mt-4">

          <div
            className={`${strengthColor} h-4 rounded-full transition-all duration-500`}
            style={{
              width: `${portfolioStrength}%`,
            }}
          />

        </div>

        {/* Explanation */}

        <div className="mt-4">

          <p
            className={`text-sm font-medium ${strengthTextColor}`}
          >
            {portfolioStrength >= 80 &&
              "✅ Your portfolio has a strong overall structure."}

            {portfolioStrength >= 60 &&
              portfolioStrength < 80 &&
              "⚡ Your portfolio is reasonably structured, but some improvements may be useful."}

            {portfolioStrength >= 40 &&
              portfolioStrength < 60 &&
              "⚠️ Your portfolio has weaknesses that should be addressed."}

            {portfolioStrength < 40 &&
              "🚨 Your portfolio has significant structural weaknesses and concentration risk."}
          </p>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Score Cards */}
      {/* -------------------------------- */}

      <div className="grid md:grid-cols-3 gap-4">

        {/* Health */}

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Portfolio Health
          </p>

          <p className="text-3xl font-bold mt-2">
            {healthScore}/100
          </p>

          <p className="text-sm text-gray-500 mt-1">
            Overall portfolio condition
          </p>

        </div>

        {/* Risk */}

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Portfolio Risk Score
          </p>

          <p className="text-3xl font-bold mt-2">
            {portfolioRiskScore}/100
          </p>

          <p className="text-sm text-gray-500 mt-1">
            Higher score = lower risk
          </p>

        </div>

        {/* Diversification */}

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Sector Diversification
          </p>

          <p className="text-3xl font-bold mt-2">
            {sectorScore}/100
          </p>

          <p className="text-sm text-gray-500 mt-1">
            Sector diversification quality
          </p>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Risk Gauge */}
      {/* -------------------------------- */}

      <div className="border rounded-xl p-5 mt-6">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-gray-500">
              Portfolio Risk Level
            </p>

            <p className="text-2xl font-bold mt-1">
              {riskGaugeLabel}
            </p>

          </div>

          <div className="text-right">

            <p className="text-3xl font-bold">
              {portfolioRiskScore}/100
            </p>

            <p className="text-sm text-gray-500">
              Risk Safety Score
            </p>

          </div>

        </div>

        {/* Gauge */}

        <div className="w-full bg-gray-200 rounded-full h-4 mt-4">

          <div
            className={`${riskGaugeColor} h-4 rounded-full transition-all duration-500`}
            style={{
              width: `${portfolioRiskScore}%`,
            }}
          />

        </div>

        <div className="flex justify-between text-xs text-gray-500 mt-2">

          <span>Very High Risk</span>

          <span>High</span>

          <span>Medium</span>

          <span>Low Risk</span>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Risk Information */}
      {/* -------------------------------- */}

      <div className="grid md:grid-cols-3 gap-4 mt-6">

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Risk Level
          </p>

          <p className="text-xl font-bold mt-2">
            {advisor.risk}
          </p>

        </div>

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Portfolio Risk
          </p>

          <p className="text-xl font-bold mt-2">
            {advisor.portfolio_risk}
          </p>

        </div>

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Diversification
          </p>

          <p className="text-xl font-bold mt-2">
            {advisor.diversification}
          </p>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Risk Breakdown */}
      {/* -------------------------------- */}

      <div className="mt-6">

        <h3 className="text-lg font-bold mb-4">
          ⚠️ Portfolio Risk Breakdown
        </h3>

        <div className="grid md:grid-cols-3 gap-4">

          {/* Largest Holding */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Largest Holding
            </p>

            <p className="text-xl font-bold mt-2">
              {advisor.largest_holding}
            </p>

            <p className="text-sm text-gray-500 mt-1">
              {largestHoldingPercent.toFixed(2)}%
              {" "}
              of portfolio
            </p>

          </div>

          {/* Largest Sector */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Largest Sector
            </p>

            <p className="text-xl font-bold mt-2">
              {largestSector}
            </p>

            <p className="text-sm text-gray-500 mt-1">
              {largestSectorPercentage.toFixed(2)}%
              {" "}
              of portfolio
            </p>

          </div>

          {/* Sector Count */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Sectors
            </p>

            <p className="text-xl font-bold mt-2">
              {sectorCount}
            </p>

            <p className="text-sm text-gray-500 mt-1">
              {advisor.diversification}
            </p>

          </div>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Risk Warning */}
      {/* -------------------------------- */}

      <div className="mt-6">

        {advisor.portfolio_risk === "Very High" && (

          <div className="bg-red-50 border border-red-200 rounded-xl p-5">

            <h3 className="font-bold text-red-700">
              🚨 Very High Concentration Risk
            </h3>

            <p className="text-red-600 mt-2">
              Your portfolio has significant concentration
              risk. Your largest holding represents a large
              percentage of the portfolio.
            </p>

          </div>

        )}

        {advisor.portfolio_risk === "High" && (

          <div className="bg-orange-50 border border-orange-200 rounded-xl p-5">

            <h3 className="font-bold text-orange-700">
              ⚠️ Elevated Portfolio Risk
            </h3>

            <p className="text-orange-600 mt-2">
              Your portfolio has noticeable concentration.
              Consider improving diversification.
            </p>

          </div>

        )}

        {advisor.portfolio_risk === "Medium" && (

          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-5">

            <h3 className="font-bold text-yellow-700">
              ⚡ Moderate Portfolio Risk
            </h3>

            <p className="text-yellow-700 mt-2">
              Your portfolio has moderate concentration.
              Continue monitoring diversification.
            </p>

          </div>

        )}

        {advisor.portfolio_risk === "Low" && (

          <div className="bg-green-50 border border-green-200 rounded-xl p-5">

            <h3 className="font-bold text-green-700">
              ✅ Healthy Portfolio Structure
            </h3>

            <p className="text-green-700 mt-2">
              Your portfolio appears reasonably diversified.
            </p>

          </div>

        )}

      </div>

      {/* -------------------------------- */}
      {/* Holdings */}
      {/* -------------------------------- */}

      <div className="grid md:grid-cols-3 gap-4 mt-6">

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Largest Holding
          </p>

          <p className="text-xl font-bold mt-2">
            {advisor.largest_holding}
          </p>

        </div>

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Largest Holding %
          </p>

          <p className="text-xl font-bold mt-2">
            {largestHoldingPercent.toFixed(2)}%
          </p>

        </div>

        <div className="border rounded-xl p-4">

          <p className="text-gray-500">
            Total Holdings
          </p>

          <p className="text-xl font-bold mt-2">
            {totalHoldings}
          </p>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Portfolio Performance */}
      {/* -------------------------------- */}

      <div className="mt-6">

        <h3 className="text-lg font-bold mb-4">
          📊 Portfolio Performance
        </h3>

        <div className="grid md:grid-cols-4 gap-4">

          {/* Investment */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Investment
            </p>

            <p className="text-xl font-bold mt-2">
              ₹
              {Number(
                advisor.total_investment || 0
              ).toFixed(2)}
            </p>

          </div>

          {/* Current Value */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Current Value
            </p>

            <p className="text-xl font-bold mt-2">
              ₹
              {Number(
                advisor.current_value || 0
              ).toFixed(2)}
            </p>

          </div>

          {/* Profit */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Profit
            </p>

            <p
              className={`text-xl font-bold mt-2 ${
                Number(advisor.profit || 0) >= 0
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              ₹
              {Number(
                advisor.profit || 0
              ).toFixed(2)}
            </p>

          </div>

          {/* Profit % */}

          <div className="border rounded-xl p-4">

            <p className="text-gray-500">
              Profit %
            </p>

            <p
              className={`text-xl font-bold mt-2 ${
                profitPercent >= 0
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {profitPercent.toFixed(2)}%
            </p>

          </div>

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Sector Allocation */}
      {/* -------------------------------- */}

      <div className="mt-6">

        <h3 className="text-lg font-bold mb-4">
          🏭 Sector Allocation
        </h3>

        <div className="space-y-3">

          {advisor.sectors &&
            Object.entries(
              advisor.sectors
            ).map(
              ([sector, percentage]) => (

                <div key={sector}>

                  <div className="flex justify-between mb-1">

                    <span className="font-medium">
                      {sector}
                    </span>

                    <span className="font-bold">
                      {Number(
                        percentage
                      ).toFixed(2)}%
                    </span>

                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-3">

                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      style={{
                        width: `${Number(
                          percentage
                        )}%`,
                      }}
                    />

                  </div>

                </div>

              )
            )}

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Sector Pie Chart */}
      {/* -------------------------------- */}

      {sectorLabels.length > 0 && (

        <div className="mt-8">

          <h3 className="text-lg font-bold mb-4">
            📈 Sector Allocation Chart
          </h3>

          <div className="max-w-md mx-auto">

            <Pie
              data={sectorChartData}
              options={sectorChartOptions}
            />

          </div>

        </div>

      )}

      {/* -------------------------------- */}
      {/* AI Recommendation */}
      {/* -------------------------------- */}

      <div className="mt-8 bg-gray-50 rounded-xl p-5">

        <h3 className="text-lg font-bold mb-2">
          💡 AI Recommendation
        </h3>

        <p className="text-gray-700">
          {advisor.recommendation}
        </p>

      </div>

      {/* -------------------------------- */}
      {/* Recommended Actions */}
      {/* -------------------------------- */}

      <div className="mt-6 border rounded-xl p-5">

        <h3 className="text-lg font-bold mb-4">
          🎯 Recommended Actions
        </h3>

        <div className="space-y-3">

          {recommendedActions.map(
            (action, index) => (

              <div
                key={index}
                className={`flex items-start gap-3 rounded-lg p-4 ${
                  index === 0
                    ? "bg-red-50 border border-red-200"
                    : "bg-gray-50"
                }`}
              >

                <div
                  className={`font-bold ${
                    index === 0
                      ? "text-red-600"
                      : "text-blue-600"
                  }`}
                >
                  {index + 1}.
                </div>

                <p
                  className={
                    index === 0
                      ? "text-red-700 font-medium"
                      : "text-gray-700"
                  }
                >
                  {action}
                </p>

              </div>

            )
          )}

        </div>

      </div>

    </div>
  );
}