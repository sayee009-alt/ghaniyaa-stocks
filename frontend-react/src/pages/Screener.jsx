import { useEffect, useState } from "react";

function Screener() {
  const [stocks, setStocks] = useState([]);
  const [search, setSearch] = useState("");
  const [sectorFilter, setSectorFilter] = useState("All");
  const [sortBy, setSortBy] = useState("score");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadScreener() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          "http://127.0.0.1:8000/screener?limit=50"
        );

        if (!response.ok) {
          throw new Error(
            `Screener API failed: ${response.status}`
          );
        }

        const data = await response.json();

        console.log("Screener API response:", data);

        if (Array.isArray(data)) {
          setStocks(data);
        } else {
          setStocks(data?.stocks || []);
        }
      } catch (err) {
        console.error("Screener error:", err);
        setError(err.message || "Unable to load screener");
        setStocks([]);
      } finally {
        setLoading(false);
      }
    }

    loadScreener();
  }, []);

  const sectors = [
    "All",
    ...Array.from(
      new Set(
        stocks
          .map((stock) => stock.sector)
          .filter(
            (sector) =>
              sector &&
              sector !== "Unknown"
          )
      )
    ).sort(),
  ];

  const filteredStocks = stocks
    .filter((stock) => {
      const symbol = String(
        stock.symbol || ""
      ).toLowerCase();

      const company = String(
        stock.company || ""
      ).toLowerCase();

      const searchText =
        search.toLowerCase();

      const matchesSearch =
        symbol.includes(searchText) ||
        company.includes(searchText);

      const matchesSector =
        sectorFilter === "All" ||
        stock.sector === sectorFilter;

      return (
        matchesSearch &&
        matchesSector
      );
    })
    .sort((a, b) => {
      if (sortBy === "score") {
        return (
          Number(b.score ?? -Infinity) -
          Number(a.score ?? -Infinity)
        );
      }

      if (sortBy === "price") {
        return (
          Number(b.price ?? -Infinity) -
          Number(a.price ?? -Infinity)
        );
      }

      if (sortBy === "pe") {
        return (
          Number(a.pe ?? 9999) -
          Number(b.pe ?? 9999)
        );
      }

      if (sortBy === "marketCap") {
        return (
          Number(b.marketCap ?? -Infinity) -
          Number(a.marketCap ?? -Infinity)
        );
      }

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

        {/* FILTERS */}

        <div className="flex flex-wrap gap-4 mb-6">

          <input
            type="text"
            placeholder="Search stock..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
            className="border rounded-lg p-2 w-64 bg-white"
          />

          <select
            value={sectorFilter}
            onChange={(e) =>
              setSectorFilter(e.target.value)
            }
            className="border rounded-lg p-2 bg-white"
          >
            {sectors.map((sector) => (
              <option
                key={sector}
                value={sector}
              >
                {sector}
              </option>
            ))}
          </select>

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(e.target.value)
            }
            className="border rounded-lg p-2 bg-white"
          >
            <option value="score">
              Sort by Score
            </option>

            <option value="price">
              Sort by Price
            </option>

            <option value="pe">
              Sort by PE Ratio
            </option>

            <option value="marketCap">
              Sort by Market Cap
            </option>
          </select>

        </div>

        {/* STATUS */}

        {loading && (
          <div className="bg-white rounded-xl shadow p-6 mb-6">
            <p className="text-gray-600">
              Loading screener...
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-300 text-red-700 rounded-xl p-4 mb-6">
            <strong>Screener Error:</strong>{" "}
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          stocks.length === 0 && (
            <div className="bg-white rounded-xl shadow p-6">
              <p className="text-gray-500">
                No stocks available.
              </p>
            </div>
          )}

        {/* TABLE */}

        {!loading &&
          stocks.length > 0 && (
            <div className="bg-white rounded-xl shadow overflow-x-auto">

              <table className="w-full">

                <thead className="bg-blue-600 text-white">

                  <tr>
                    <th className="p-3 text-left">
                      Rank
                    </th>

                    <th className="p-3 text-left">
                      Symbol
                    </th>

                    <th className="p-3 text-left">
                      Company
                    </th>

                    <th className="p-3 text-right">
                      Price
                    </th>

                    <th className="p-3 text-left">
                      Sector
                    </th>

                    <th className="p-3 text-right">
                      PE
                    </th>

                    <th className="p-3 text-right">
                      ROE
                    </th>

                    <th className="p-3 text-right">
                      Score
                    </th>
                  </tr>

                </thead>

                <tbody>

                  {filteredStocks.map(
                    (stock) => (

                      <tr
                        key={stock.symbol}
                        className="border-b hover:bg-gray-100"
                      >

                        <td className="p-3">
                          {stock.rank ?? "-"}
                        </td>

                        <td className="p-3 font-bold">
                          {stock.symbol}
                        </td>

                        <td className="p-3">
                          {stock.company ||
                            "Unknown"}
                        </td>

                        <td className="p-3 text-right">
                          {stock.price != null
                            ? `₹${Number(
                                stock.price
                              ).toLocaleString(
                                "en-IN",
                                {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2,
                                }
                              )}`
                            : "-"}
                        </td>

                        <td className="p-3">
                          {stock.sector ||
                            "Unknown"}
                        </td>

                        <td className="p-3 text-right">
                          {stock.pe != null
                            ? Number(
                                stock.pe
                              ).toFixed(2)
                            : "-"}
                        </td>

                        <td className="p-3 text-right">
                          {stock.roe != null
                            ? Number(
                                stock.roe
                              ).toFixed(4)
                            : "-"}
                        </td>

                        <td className="p-3 text-right">

                          <span
                            className={
                              `px-3 py-1 rounded-full text-white font-bold ` +
                              (
                                stock.score >= 90
                                  ? "bg-green-600"
                                  : stock.score >= 75
                                  ? "bg-blue-600"
                                  : stock.score >= 60
                                  ? "bg-yellow-500"
                                  : "bg-red-600"
                              )
                            }
                          >
                            {stock.score ?? "-"}
                          </span>

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>
          )}

        {!loading &&
          !error &&
          stocks.length > 0 &&
          filteredStocks.length === 0 && (
            <div className="bg-white rounded-xl shadow p-6 mt-4">
              <p className="text-gray-500">
                No stocks match your search or sector filter.
              </p>
            </div>
          )}

      </div>
    </div>
  );
}

export default Screener;