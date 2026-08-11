import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

function CompareChart({ comparison }) {
  if (!comparison) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p className="text-gray-500">
          Compare two stocks to view performance chart.
        </p>
      </div>
    );
  }

  const stock1 = comparison.stock1;
  const stock2 = comparison.stock2;

  if (!stock1 || !stock2) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p className="text-gray-500">
          Comparison data is incomplete.
        </p>
      </div>
    );
  }

  if (
    !stock1.history ||
    !stock2.history ||
    !stock1.history.dates ||
    !stock2.history.dates ||
    !stock1.history.prices ||
    !stock2.history.prices
  ) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p className="text-gray-500">
          Loading comparison chart...
        </p>
      </div>
    );
  }

  const data = stock1.history.dates.map((date, index) => ({
    date,
    stock1: stock1.history.prices[index],
    stock2: stock2.history.prices[index],
  }));

  return (
    <div className="bg-white p-6 rounded shadow">

      <h2 className="text-2xl font-bold mb-4">
        📈 Performance Comparison
      </h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="date"
          />

          <YAxis />

          <Tooltip />

          <Legend />

          <Line
            type="monotone"
            dataKey="stock1"
            name={stock1.symbol}
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="stock2"
            name={stock2.symbol}
            stroke="#16a34a"
            strokeWidth={2}
            dot={false}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}

export default CompareChart;