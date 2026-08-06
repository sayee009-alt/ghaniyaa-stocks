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

function CompareChart({ stock1, stock2 }) {
  if (!stock1 || !stock2) {
    return (
      <div className="bg-white p-6 rounded shadow">
        Compare two stocks to view performance chart.
      </div>
    );
  }
if (
  !stock1?.history?.dates ||
  !stock2?.history?.dates
) {
  return (
    <div className="bg-white p-6 rounded shadow">
      Loading comparison chart...
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
      <h2 className="text-xl font-bold mb-4">
        📈 Performance Comparison
      </h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="date" />

          <YAxis />

          <Tooltip />

          <Legend />

          <Line
            type="monotone"
            dataKey="stock1"
            name={stock1.symbol}
            stroke="#2563eb"
          />

          <Line
            type="monotone"
            dataKey="stock2"
            name={stock2.symbol}
            stroke="#16a34a"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CompareChart;