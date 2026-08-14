const API_BASE = "http://127.0.0.1:8000";

export async function getLiveStock(symbol) {
  const response = await fetch(`${API_BASE}/live/${symbol}`);
  return await response.json();
}

export async function getScore(symbol) {
  const response = await fetch(`${API_BASE}/score/${symbol}`);
  return await response.json();
}

export async function getHistory(symbol) {
  const response = await fetch(`${API_BASE}/history/${symbol}`);
  return await response.json();
}

export async function getSummary(symbol) {
  const response = await fetch(`${API_BASE}/summary/${symbol}`);
  return await response.json();
}

export async function getWatchlist() {
  const response = await fetch(`${API_BASE}/watchlist`);
  return await response.json();
}
export async function getFinancials(symbol) {
  const response = await fetch(`${API_BASE}/financials/${symbol}`);
  return await response.json();
}
export async function addToWatchlist(symbol) {
  const response = await fetch(`${API_BASE}/watchlist/${symbol}`, {
    method: "POST",
  });

  return await response.json();
}
export async function compareStocks(symbol1, symbol2) {
  const response = await fetch(
    `${API_BASE}/compare/${symbol1}/${symbol2}`
  );

  return await response.json();
}
export async function getNews(symbol) {
  const response = await fetch(`${API_BASE}/news/${symbol}`);
  return await response.json();
}
export async function getScreener(limit = 20) {
  const response = await fetch(
    `${API_BASE}/screener?limit=${limit}`
  );

  if (!response.ok) {
    throw new Error(
      `Screener API failed: ${response.status}`
    );
  }

  return await response.json();
}

export async function addPortfolio(stock) {
  console.log("BUY API REQUEST:", stock);

  let response;

  try {
    response = await fetch(`${API_BASE}/portfolio`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(stock),
    });
  } catch (error) {
    console.error("BUY NETWORK ERROR:", error);

    throw new Error(
      "Unable to connect to the backend. Make sure FastAPI is running on http://127.0.0.1:8000."
    );
  }

  const data = await response.json();

  console.log("BUY API RESPONSE:", data);

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Portfolio buy failed: HTTP ${response.status}`
    );
  }

  return data;
}


export async function getPortfolio() {
  console.log("GET PORTFOLIO API REQUEST");

  let response;

  try {
    response = await fetch(`${API_BASE}/portfolio`);
  } catch (error) {
    console.error("GET PORTFOLIO NETWORK ERROR:", error);

    throw new Error(
      "Unable to connect to the portfolio backend."
    );
  }

  const data = await response.json();

  console.log("GET PORTFOLIO API RESPONSE:", data);

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Portfolio request failed: HTTP ${response.status}`
    );
  }

  return data;
}
export async function sellPortfolio(stock) {
  console.log("SELL API REQUEST:", stock);

  let response;

  try {
    response = await fetch(
      `${API_BASE}/portfolio/sell`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(stock),
      }
    );
  } catch (error) {
    console.error("SELL NETWORK ERROR:", error);

    throw new Error(
      "Unable to connect to the portfolio backend."
    );
  }

  const data = await response.json();

  console.log("SELL API RESPONSE:", data);

  if (!response.ok) {
    throw new Error(
      data.detail ||
      `Unable to sell stock: HTTP ${response.status}`
    );
  }

  return data;
}
export async function getAdvisor() {
  const response = await fetch(`${API_BASE}/advisor`);

  if (!response.ok) {
    throw new Error(`Advisor API failed: ${response.status}`);
  }

  return await response.json();
}
export async function getPrediction(symbol) {
  const response = await fetch(
    `http://127.0.0.1:8000/prediction/${symbol}`
  );

  if (!response.ok) {
    throw new Error("Prediction API failed");
  }

  return await response.json();
}

export async function getDecision(symbol) {
  const response = await fetch(
    `${API_BASE}/decision/${symbol}`
  );

  if (!response.ok) {
    throw new Error("Decision API failed");
  }

  return await response.json();
}


export async function getThesis(symbol) {
  const response = await fetch(
    `${API_BASE}/thesis/${symbol}`
  );

  if (!response.ok) {
    throw new Error("Thesis API failed");
  }

  return await response.json();
}
export async function getStockAnalysis(symbol) {
  const response = await fetch(
    `http://127.0.0.1:8000/analysis/${encodeURIComponent(symbol)}`
  );

  if (!response.ok) {
    throw new Error(
      `Stock analysis request failed: ${response.status}`
    );
  }

  return await response.json();
}