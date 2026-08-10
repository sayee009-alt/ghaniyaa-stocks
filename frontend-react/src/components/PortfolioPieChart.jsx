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

function PortfolioPieChart({ portfolio }) {

  console.log("PortfolioPieChart:", portfolio);

  if (!portfolio) {
    return null;
  }

  const holdings = portfolio.holdings || [];

  if (holdings.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-2xl font-bold mb-4">
          📊 Portfolio Allocation
        </h2>

        <p className="text-gray-500">
          No portfolio holdings available.
        </p>
      </div>
    );
  }

  // --------------------------------
  // Prepare chart data
  // --------------------------------

  const labels = holdings.map(
    (holding) =>
      holding.symbol ||
      holding.stock ||
      holding.name ||
      "Unknown"
  );

  const values = holdings.map((holding) => {

    const quantity = Number(
      holding.quantity || 0
    );

    const currentPrice = Number(
      holding.currentPrice ||
      holding.current_price ||
      holding.price ||
      holding.buyPrice ||
      holding.buy_price ||
      0
    );

    return quantity * currentPrice;
  });

  // --------------------------------
  // Chart data
  // --------------------------------

  const chartData = {
    labels,

    datasets: [
      {
        label: "Portfolio Allocation",

        data: values,

        borderWidth: 1,

        // Important:
        // No fill:true here because this is a Pie chart.
      },
    ],
  };

  // --------------------------------
  // Chart options
  // --------------------------------

  const chartOptions = {
    responsive: true,

    maintainAspectRatio: false,

    plugins: {

      legend: {
        position: "bottom",
      },

      tooltip: {
        callbacks: {
          label: function (context) {

            const value = Number(
              context.raw || 0
            );

            const total = values.reduce(
              (sum, item) => sum + item,
              0
            );

            const percentage =
              total > 0
                ? ((value / total) * 100).toFixed(2)
                : 0;

            return `${context.label}: ₹${value.toFixed(
              2
            )} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-xl shadow p-6">

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-2xl font-bold">
            📊 Portfolio Allocation
          </h2>

          <p className="text-gray-500 mt-1">
            Current portfolio distribution by holding
          </p>

        </div>

        <div className="text-right">

          <p className="text-sm text-gray-500">
            Holdings
          </p>

          <p className="text-2xl font-bold">
            {holdings.length}
          </p>

        </div>

      </div>

      <div
        className="relative"
        style={{
          height: "350px",
        }}
      >

        <Pie
          data={chartData}
          options={chartOptions}
        />

      </div>

    </div>
  );
}

export default PortfolioPieChart;