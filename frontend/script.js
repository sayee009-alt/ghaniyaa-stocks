let stockChart = null;
async function analyzeStock() {

    const symbol = document.getElementById("stockInput").value.toUpperCase();

    try {

        const response = await fetch(`http://127.0.0.1:8000/live/${symbol}`);

        const data = await response.json();

        document.getElementById("company").textContent = data.company;
        document.getElementById("price").textContent = "₹ " + data.price;
        document.getElementById("sector").textContent = data.sector;
        document.getElementById("marketCap").textContent = data.marketCap;
        const scoreResponse = await fetch(`http://127.0.0.1:8000/score/${symbol}`);
const scoreData = await scoreResponse.json();
const summaryResponse = await fetch(`http://127.0.0.1:8000/summary/${symbol}`);
const summaryData = await summaryResponse.json();

document.getElementById("summary").textContent = summaryData.summary;


document.getElementById("score").textContent =
    scoreData.ghaniyaa_score + " / 100";
    const historyResponse = await fetch(`http://127.0.0.1:8000/history/${symbol}`);
const historyData = await historyResponse.json();

const ctx = document.getElementById("stockChart").getContext("2d");

if (stockChart) {
    stockChart.destroy();
}

stockChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: historyData.dates,
        datasets: [{
            label: `${symbol} Closing Price`,
            data: historyData.prices
        }]
    },
    options: {
        responsive: true
    }
});

    } catch (error) {

        alert("Unable to fetch stock data.");

    }

}