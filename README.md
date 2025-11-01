🏆 Gold Price Forecasting Dashboard (INR)

📘 Overview

The Gold Price Forecasting Dashboard is an interactive data science project built with Python and Streamlit that provides real-time gold price insights and 15-day forecasts in Indian Rupees (₹).
It fetches live gold market data from Yahoo Finance, converts values from USD to INR, and displays prices for 8 grams (1 Savaran) — a popular unit of gold in India.

🚀 Features

✅ Real-time gold price tracking (USD → INR conversion)
✅ Live visualization for 8 grams (1 Savaran)
✅ Historical analysis (15 days, 1 month, and yearly trends)
✅ 15-day gold price prediction using Machine Learning (Linear Regression)
✅ Interactive dashboards with Plotly charts
✅ Moving Average trendlines for better insights

🛠️ Tech Stack

Python 3.9+

Streamlit – interactive dashboard

yFinance – fetch live market data

Plotly – dynamic charts

scikit-learn – prediction model

Pandas / NumPy – data processing

⚙️ Installation
# Clone the repository
git clone (https://github.com/kavikkuyil/gold_price-forecasting.git)
cd gold-price-forecasting

# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install streamlit pandas numpy yfinance matplotlib scikit-learn


▶️ Run the Dashboard
streamlit run gold_forecasting.py


Then open the URL shown in your terminal (usually http://localhost:8501
).
