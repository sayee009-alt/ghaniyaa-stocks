import { useState, useEffect } from "react";

import SearchBar from "../components/SearchBar";
import StockCard from "../components/StockCard";
import StockChart from "../components/StockChart";
import SummaryCard from "../components/SummaryCard";
import Watchlist from "../components/Watchlist";
import FinancialCard from "../components/FinancialCard";
import RecommendationCard from "../components/RecommendationCard";
import NewsCard from "../components/NewsCard";
import ScreenerTable from "../components/ScreenerTable";
import CompareCard from "../components/CompareCard";
import CompareChart from "../components/CompareChart";
import PortfolioBuilder from "../components/PortfolioBuilder";
import PortfolioCard from "../components/PortfolioCard";
import PortfolioPieChart from "../components/PortfolioPieChart";
import AdvisorCard from "../components/AdvisorCard";
import PredictionCard from "../components/PredictionCard";
import DecisionCard from "../components/DecisionCard";
import ThesisCard from "../components/ThesisCard";
import { getStockAnalysis } from "../services/api";
import StockAnalysisCard from "../components/StockAnalysisCard";

import {
  getLiveStock,
  getScore,
  getHistory,
  getSummary,
  getFinancials,
  getScreener,
  getWatchlist,
  addToWatchlist,
  compareStocks,
  getPortfolio,
  addPortfolio,
  sellPortfolio,
  getPrediction,
  getDecision,
  getThesis,
  getNews,
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
  const [symbol1, setSymbol1] = useState("");
  const [symbol2, setSymbol2] = useState("");
  const [comparison, setComparison] = useState(null);

  const [portfolio, setPortfolio] = useState({
    holdings: [],
    totalInvestment: 0,
    currentValue: 0,
    profit: 0,
  });

  const [prediction, setPrediction] = useState(null);
  const [decision, setDecision] = useState(null);
  const [thesis, setThesis] = useState(null);

  const [selectedStock, setSelectedStock] = useState(null);
  const [stockAnalysis, setStockAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  // ============================================================
  // MAIN STOCK ANALYSIS
  // ============================================================

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

      const predictionData = await getPrediction(upperSymbol);
      console.log("Prediction API:", predictionData);
      setPrediction(predictionData);

      const decisionData = await getDecision(upperSymbol);
      console.log("Decision API:", decisionData);
      setDecision(decisionData);

      const thesisData = await getThesis(upperSymbol);
      console.log("Thesis API:", thesisData);
      setThesis(thesisData);

      const newsData = await getNews(upperSymbol);
      setNews(newsData.news);

      const financialData = await getFinancials(upperSymbol);
      setFinancials(financialData);

      await addToWatchlist(upperSymbol);

      const watchlistData = await getWatchlist();
      setWatchlist(watchlistData.watchlist);

    } catch (error) {
      console.error("Analyze Error:", error);
      alert(error.message);
    }
  }

  // ============================================================
  // STOCK ANALYSIS FROM SCREENER
  // ============================================================

  async function handleSelectStock(symbol) {
    setSelectedStock(symbol);
    setStockAnalysis(null);
    setAnalysisLoading(true);

    try {
      const data = await getStockAnalysis(symbol);

      console.log("Stock Analysis API:", data);

      setStockAnalysis(data);
    } catch (error) {
      console.error(
        "Stock Analysis API error:",
        error
      );

      setStockAnalysis({
        success: false,
        symbol,
        error: "Unable to load stock analysis.",
      });
    } finally {
      setAnalysisLoading(false);
    }
  }

  // ============================================================
  // PORTFOLIO
  // ============================================================

async function addPortfolioStock(stock) {
  try {
    await addPortfolio(stock);

    const portfolioData = await getPortfolio();

    console.log("Portfolio after BUY:", portfolioData);

    setPortfolio(portfolioData);

  } catch (error) {
    console.error("Buy Error:", error);
    alert(error.message);
  }
}


async function sellPortfolioStock(stock) {
  try {
    console.log("SELL REQUEST:", stock);

    const result = await sellPortfolio(stock);

    console.log("SELL RESPONSE:", result);

    // Reload portfolio after successful sale
    const portfolioData = await getPortfolio();

    console.log("Portfolio after SELL:", portfolioData);

    setPortfolio(portfolioData);

    alert(
      `Sold ${stock.quantity} ${stock.symbol} successfully.\n` +
      `Realized Profit: ₹${result.realizedProfit}`
    );

  } catch (error) {

    console.error("Sell Error:", error);

    alert(
      error.message ||
      "Unable to sell stock."
    );
  }
}

  // ============================================================
  // COMPARE
  // ============================================================

  async function compare() {
    try {
      const data = await compareStocks(
        symbol1,
        symbol2
      );

      console.log(data);

      setComparison(data);
    } catch (error) {
      console.error(error);
    }
  }

  // ============================================================
  // LOAD DASHBOARD
  // ============================================================

  useEffect(() => {
    async function loadDashboard() {
      try {
        const screenerData = await getScreener(20);

        /*
         * Your backend returns:
         *
         * {
         *   stocks: [...],
         *   count: 17,
         *   invalidCount: 1,
         *   invalid: [...]
         * }
         *
         * Keep only the stocks array for ScreenerTable.
         */

        if (Array.isArray(screenerData)) {
          setScreener(screenerData);
        } else {
          setScreener(
            screenerData?.stocks || []
          );
        }

        const portfolioData = await getPortfolio();

        setPortfolio(portfolioData);

      } catch (error) {
        console.error(error);
      }
    }

    loadDashboard();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="max-w-7xl mx-auto p-6">

        {/* ======================================================
            HEADER
        ====================================================== */}

        <h1 className="text-4xl font-bold">
          📈 Ghaniyaa Stocks
        </h1>

        <p className="text-gray-600 mt-2">
          AI-Powered Investment Research Platform
        </p>

        {/* ======================================================
            SEARCH
        ====================================================== */}

        <div className="mt-8">
          <SearchBar onAnalyze={analyzeStock} />
        </div>

        {/* ======================================================
            STOCK SCREENER
        ====================================================== */}

        <div className="mt-8 bg-white p-6 rounded shadow">

          <ScreenerTable
            stocks={screener}
            onSelectStock={handleSelectStock}
          />

        </div>

<StockAnalysisCard
  analysis={stockAnalysis}
  loading={analysisLoading}
  onClose={() => {
    setSelectedStock(null);
    setStockAnalysis(null);
  }}
/>
    



{/* STOCK */}
    <div className="mt-8">
      <StockCard
        stock={stock}
        score={score}
      />
    </div>

    
        {/* ======================================================
            FINANCIALS
        ====================================================== */}

        <div className="mt-8">
          <FinancialCard
            financials={financials}
          />
        </div>


    {/* STOCK CHART */}
    <div className="mt-8">
      <StockChart history={history} />
    </div>



        {/* ======================================================
            RECOMMENDATION
        ====================================================== */}

        <div className="mt-8">
          <RecommendationCard
            score={score}
          />
        </div>

        {/* ======================================================
            PREDICTION
        ====================================================== */}

        <div className="mt-8">
          <PredictionCard
            prediction={prediction}
          />
        </div>

        {/* ======================================================
            DECISION
        ====================================================== */}

        <div className="mt-8">
          <DecisionCard
            decision={decision}
          />
        </div>

        {/* ======================================================
            THESIS
        ====================================================== */}

        <div className="mt-8">
          <ThesisCard
            thesis={thesis}
          />
        </div>

        {/* ======================================================
            SUMMARY
        ====================================================== */}

        <div className="mt-8">
          <SummaryCard
            summary={summary}
          />
        </div>

        {/* ======================================================
            NEWS
        ====================================================== */}

        <div className="mt-8">
          <NewsCard
            news={news}
          />
        </div>

        {/* ======================================================
            COMPARE
        ====================================================== */}

<div className="mt-8 bg-white p-6 rounded shadow">
<h2 className="text-2xl font-bold mb-4">
    🔄 Compare Stocks
  </h2>
  <div className="flex gap-4">

    <input
      type="text"
      placeholder="First Symbol"
      value={symbol1}
      onChange={(e) =>
        setSymbol1(
          e.target.value.toUpperCase()
        )
      }
      className="border p-2 rounded flex-1"
    />

    <input
      type="text"
      placeholder="Second Symbol"
      value={symbol2}
      onChange={(e) =>
        setSymbol2(
          e.target.value.toUpperCase()
        )
      }
      className="border p-2 rounded flex-1"
    />

    <button
      onClick={compare}
      className="bg-blue-600 text-white px-4 rounded"
    >
      Compare
    </button>

  </div>

  {comparison && (
    <div className="mt-6">
      <CompareCard comparison={comparison} />
    </div>
  )}

  {comparison && (
    <div className="mt-6">
      <CompareChart comparison={comparison} />
    </div>
  )}

</div>


        {/* ======================================================
    PORTFOLIO BUILDER
====================================================== */}

<div className="mt-8">
  <PortfolioBuilder
    onAdd={addPortfolioStock}
  />
</div>

{/* ======================================================
    PORTFOLIO DASHBOARD
====================================================== */}

<div className="mt-8">
 <PortfolioCard
  portfolio={portfolio}
  onSell={sellPortfolioStock}
  onPortfolioUpdated={async () => {
    const portfolioData = await getPortfolio();
    setPortfolio(portfolioData);
  }}
/>
</div>

        {/* ======================================================
            PORTFOLIO PIE
        ====================================================== */}

        <div className="mt-8">
          <PortfolioPieChart
            portfolio={portfolio}
          />
        </div>

        {/* ======================================================
            ADVISOR
        ====================================================== */}

        <div className="mt-8">
          <AdvisorCard />
        </div>


        {/* ======================================================
            WATCHLIST
        ====================================================== */}

        <div className="mt-8">
          <Watchlist
            watchlist={watchlist}
          />
        </div>

      </div>
    </div>
  );
}

export default Dashboard;