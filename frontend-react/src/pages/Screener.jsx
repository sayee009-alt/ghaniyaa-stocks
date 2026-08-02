import { useEffect, useState } from "react";

function Screener() {
  const [stocks, setStocks] = useState([]);
const [search, setSearch] = useState("");
const [sectorFilter, setSectorFilter] = useState("All");
const [sortBy, setSortBy] = useState("score");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/screener")
      .then((res) => res.json())
      .then((data) => setStocks(data))
      .catch((err) => console.error(err));
  }, []);

  const filteredStocks = stocks
  .filter((stock) => {
    const matchesSearch =
      stock.symbol.toLowerCase().includes(search.toLowerCase()) ||
      stock.company.toLowerCase().includes(search.toLowerCase());

    const matchesSector =
      sectorFilter === "All" ||
      stock.sector === sectorFilter;

    return matchesSearch && matchesSector;
  })
  .sort((a, b) => {
    if (sortBy === "score") return b.score - a.score;
    if (sortBy === "price") return b.price - a.price;
    if (sortBy === "pe") return (a.pe ?? 9999) - (b.pe ?? 9999);
    return 0;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-7xl mx-auto">

        <h1 className="text-4xl font-bold mb-2">
          📊 AI Stock Screener
        </h1>

        <p className="text-gray-600 mb-8">
          Ghaniyaa Stocks Screener
        </p>
<div className="flex flex-wrap gap-4 mb-6">

  <input
    type="text"
    placeholder="Search stock..."
    value={search}
    onChange={(e) => setSearch(e.target.value)}
    className="border rounded-lg p-2 w-64"
  />

  <select
    value={sectorFilter}
    onChange={(e) => setSectorFilter(e.target.value)}
    className="border rounded-lg p-2"
  >
    <option>All</option>
    <option>Technology</option>
    <option>Financial Services</option>
    <option>Energy</option>
    <option>Industrials</option>
    <option>Consumer Defensive</option>
  </select>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    className="border rounded-lg p-2"
  >
    <option value="score">Sort by Score</option>
    <option value="price">Sort by Price</option>
    <option value="pe">Sort by PE Ratio</option>
  </select>

</div>
        <div className="bg-white rounded-xl shadow overflow-x-auto">

          <table className="w-full">

            <thead className="bg-blue-600 text-white">

              <tr>
                <th className="p-3 text-left">Symbol</th>
                <th className="p-3 text-left">Company</th>
                <th className="p-3 text-left">Price</th>
                <th className="p-3 text-left">Sector</th>
                <th className="p-3 text-left">PE</th>
                <th className="p-3 text-left">ROE</th>
                <th className="p-3 text-left">Score</th>
              </tr>

            </thead>

            <tbody>

              {filteredStocks.map((stock) => (

                <tr
                  key={stock.symbol}
                  className="border-b hover:bg-gray-100"
                >
                  <td className="p-3 font-bold">
                    {stock.symbol}
                  </td>

                  <td className="p-3">
                    {stock.company}
                  </td>

                  <td className="p-3">
                    ₹{stock.price}
                  </td>

                  <td className="p-3">
                    {stock.sector}
                  </td>

                  <td className="p-3">
                    {stock.pe ?? "-"}
                  </td>

                  <td className="p-3">
                    {stock.roe ?? "-"}
                  </td>

                  <td className="p-3">

                    <span
                      className={`px-3 py-1 rounded-full text-white font-bold ${
                        stock.score >= 90
                          ? "bg-green-600"
                          : stock.score >= 75
                          ? "bg-blue-600"
                          : stock.score >= 60
                          ? "bg-yellow-500"
                          : "bg-red-600"
                      }`}
                    >
                      {stock.score}
                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Screener;