# 📈 AI Market Dashboard

An AI-powered financial analysis dashboard built with **Python + Streamlit** that allows users to analyze stock market data using natural language commands.

The dashboard provides price trends, technical indicators, volatility analysis, correlation analysis, AI-generated trading signals, watchlist management, and downloadable PDF reports — all inside a clean professional UI.

---

## 🚀 Live Features

- Natural language stock analysis
- Price trend visualization
- RSI (Relative Strength Index)
- Moving Averages (MA50 / MA200)
- Correlation between stocks
- Annualized volatility calculation
- AI-generated Buy / Sell / Hold signal
- Watchlist management
- PDF report export
- Professional dark-mode dashboard

---

## 🎤 Example Commands
  trend for TSLA 6 months
  volatility of AAPL 1 year
  moving average for SPY 1 year
  RSI for NVDA 6 months
  correlation AAPL and MSFT 6 months

---

## 🧠 AI Signal Logic

The dashboard generates a trading signal based on:

- Trend direction
- RSI level (overbought / oversold)
- Moving average crossover
- Volatility conditions

Signal output:
- **BUY** → Favorable technical setup
- **SELL** → Overbought or bearish indicators
- **HOLD** → Mixed or neutral signals

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- yFinance
- Custom financial analytics logic

---

## 📊 Project Structure

```
ai-market-dashboard/
│
├── src/
│   ├── finance.py      # Financial calculations
│   ├── parser.py       # Natural language command parsing
│   ├── charts.py       # Plotly chart generation
│   └── report.py       # PDF report builder
│
├── app.py              # Main Streamlit app
├── requirements.txt
├── .gitignore
└── README.md
```

  
---

## ⚡ Installation (Local Setup)

### 1️⃣ Clone the repository: https://github.com/nisarg2805/ai-market-dashboard.git


---

## 📄 PDF Report Export

Users can download a detailed AI-generated PDF report containing:

- Selected ticker
- Timeframe
- Total return
- Volatility
- AI signal
- AI reasoning

---

## 📈 Use Cases

- Personal portfolio analysis
- Educational financial learning
- Demonstrating technical indicator logic
- Showcasing Python + data visualization skills

---

## ⚠️ Disclaimer

This project is for educational and demonstration purposes only.  
It does not provide financial advice.

---

## 👨‍💻 Author

**Nisarg Rajput**

GitHub: https://github.com/nisarg2805
