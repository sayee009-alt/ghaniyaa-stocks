import { useState, useEffect } from "react";

import SearchBar from "../components/SearchBar";
import StockCard from "../components/StockCard";
import StockChart from "../components/StockChart";
import SummaryCard from "../components/SummaryCard";
import Watchlist from "../components/Watchlist";
import FinancialCard from "../components/FinancialCard";
import RecommendationCard from "../components/RecommendationCard";
import NewsCard from "../components/NewsCard";
import { getNews } from "../services/api";
import ScreenerTable from "../components/ScreenerTable";

import {
  getLiveStock,
  getScore,
  getHistory,
  getSummary,
  getFinancials,
  getScreener,
  getWatchlist,
  addToWatchlist,
} from "../services/api";

function Dashboard() {
    const [screener, setScreener] = useState([]);
  const [stock, setStock] = useState(null);
  const [score, setScore] = useState(null);
  const [history, setHistory] = useState(null);
  const [summary, setSummary] = useState(null);
  const [financials, setFinancials] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [news, setNews] = useState([]);

  async function analyzeStock(symbol) {
    try {
      const upperSymbol = symbol.toUpperCase();

      const liveData = await getLiveStock(upperSymbol);
      setStock(liveData);

      const scoreData = await getScore(upperSymbol);
      setScore(scoreData);

      const historyData = await getHistory(upperSymbol);
console.log("History API:", historyData);
setHistory(historyData);

const summaryData = await getSummary(upperSymbol);
setSummary(summaryData);

const newsData = await getNews(upperSymbol);
setNews(newsData.news);

const financialData = await getFinancials(upperSymbol);
setFinancials(financialData);

await addToWatchlist(upperSymbol);

const watchlistData = await getWatchlist();
setWatchlist(watchlistData.watchlist);

    } catch (error) {
      console.error(error);
      alert("Unable to fetch stock data.");
    }
  }

  useEffect(() => {
  async function loadScreener() {
    try {
      const data = await getScreener();
      setScreener(data);
    } catch (error) {
      console.error(error);
    }
  }

  loadScreener();
}, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">

        <h1 className="text-4xl font-bold">
          📈 Ghaniyaa Stocks
        </h1>

        <p className="text-gray-600 mt-2">
          AI-Powered Investment Research Platform
        </p>

        <div className="mt-8">
          <SearchBar onAnalyze={analyzeStock} />
        </div>

        <div className="mt-8">
          <StockCard stock={stock} score={score} />
        </div>

        <div className="mt-8">
         <FinancialCard financials={financials} />
         </div>

        <div className="mt-8">
           <RecommendationCard score={score} />  
        </div>

        

        <div className="mt-8">
          <SummaryCard summary={summary} />
        </div>

        <div className="mt-8">
        <NewsCard news={news} />
        </div>
        

        

<div className="mt-8">
          <StockChart history={history} />
        </div>

        <div className="mt-8">
  <ScreenerTable stocks={screener} />
</div>

        <div className="mt-8">
          <Watchlist watchlist={watchlist} />
        </div>

      </div>
    </div>
  );
}

export default Dashboard;