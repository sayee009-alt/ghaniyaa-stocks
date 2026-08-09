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

export default function AdvisorSectorChart({ sectors }) {

  if (!sectors || Object.keys(sectors).length === 0) {
    return null;
  }

  const labels = Object.keys(sectors);

  const values = Object.values(sectors).map(
    (value) => Number(value)
  );

  const data = {
    labels: labels,
    datasets: [
      {
        data: values,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
  };

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-6">

      <h2 className="text-xl font-bold mb-4">
        🏭 Sector Allocation
      </h2>

      <div className="max-w-md mx-auto">
        <Pie
          data={data}
          options={options}
        />
      </div>

    </div>
  );
}