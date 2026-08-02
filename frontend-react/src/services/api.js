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
  return await response.json();
}