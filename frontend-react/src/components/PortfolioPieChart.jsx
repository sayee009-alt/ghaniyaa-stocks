import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const COLORS = [
  "#2563eb",
  "#16a34a",
  "#f59e0b",
  "#dc2626",
  "#7c3aed",
];

function PortfolioPieChart({ portfolio }) {
  console.log(portfolio);
    if (
    !portfolio ||
    !portfolio.holdings ||
    portfolio.holdings.length === 0
  ) {
    return (
      <div className="bg-white p-6 rounded shadow">
        Portfolio allocation will appear here.
      </div>
    );
  }

  const data = portfolio.holdings.map((stock) => ({
    name: stock.symbol,
    value: stock.currentValue,
  }));

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">
        🥧 Portfolio Allocation
      </h2>

      <PieChart width={500} height={350}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={120}
          label
        >
          {data.map((entry, index) => (
            <Cell
              key={index}
              fill={COLORS[index % COLORS.length]}
            />
          ))}
        </Pie>

        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}

export default PortfolioPieChart;