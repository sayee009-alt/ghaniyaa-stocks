import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function StockChart({ history }) {
  if (
    !history ||
    !history.dates ||
    !history.prices ||
    history.dates.length === 0
  ) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold mb-4">
          📈 Stock Price History
        </h2>
        <p>No chart data available.</p>
      </div>
    );
  }

  const data = {
    labels: history.dates,
    datasets: [
      {
        label: "Closing Price (₹)",
        data: history.prices,
        borderColor: "#2563eb",
        backgroundColor: "rgba(37,99,235,0.2)",
        fill: true,
        tension: 0.35,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <div style={{ height: "400px" }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
}

export default StockChart;