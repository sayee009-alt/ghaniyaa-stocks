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
export async function getScreener() {
  const response = await fetch(`${API_BASE}/screener`);

  if (!response.ok) {
    throw new Error(`Screener API failed: ${response.status}`);
  }

  return await response.json();
}
export async function addPortfolio(stock) {
  const response = await fetch(`${API_BASE}/portfolio`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(stock),
  });

  return await response.json();
}

export async function getPortfolio() {
  const response = await fetch(`${API_BASE}/portfolio`);
  return await response.json();
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