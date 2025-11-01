import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------------
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="🏆 Gold Price Forecasting Dashboard (INR)",
    page_icon="🏆",
    layout="wide",
)

# -------------------------------
# 🏁 HEADER
# -------------------------------
st.title("🏆 Gold Price Forecasting Dashboard (INR)")
st.write("Track and visualize gold price trends in Indian Rupees (₹) — per 8 grams (1 Savaran).")

# -------------------------------
# ⚙️ DATE RANGE SELECTION
# -------------------------------
years = st.sidebar.slider("Select number of past years:", 1, 5, 3)
end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365 * years)).strftime('%Y-%m-%d')
st.sidebar.write(f"📅 Fetching data from: {start_date} to {end_date}")

# -------------------------------
# 📊 FETCH GOLD & EXCHANGE DATA
# -------------------------------
with st.spinner("⏳ Fetching gold price data (USD)..."):
    gold_data = yf.download("GC=F", start=start_date, end=end_date)[['Close']]
    gold_data.columns = ['Gold Price (USD)']

with st.spinner("⏳ Fetching USD to INR exchange rate..."):
    fx_data = yf.download("USDINR=X", start=start_date, end=end_date)[['Close']]
    fx_data.columns = ['USD/INR']

# -------------------------------
# 🧮 MERGE & CALCULATE INR PRICES
# -------------------------------
data = pd.merge(gold_data, fx_data, left_index=True, right_index=True, how='inner')

usd_price = data['Gold Price (USD)'].astype(float).squeeze()
usd_inr = data['USD/INR'].astype(float).squeeze()
data['Gold Price (INR)'] = usd_price.values * usd_inr.values

# Convert ounce → gram → savaran (8 grams)
data['Gold Price (8g)'] = (data['Gold Price (INR)'] / 31.1035) * 8

# -------------------------------
# 💰 CURRENT VALUES
# -------------------------------
current_8g_price = data['Gold Price (8g)'].iloc[-1]
st.success("✅ Data fetched successfully!")

col1, col2 = st.columns(2)
col1.metric("👑 Current Gold Price (INR per 8g / 1 Savaran)", f"₹ {current_8g_price:,.2f}")
col2.metric("📈 Last Updated", data.index[-1].strftime("%d %b %Y"))

# -------------------------------
# 📈 VISUALIZATION SECTION
# -------------------------------
st.subheader("📊 Gold Price Trends (8 Grams / 1 Savaran)")

# Chart 1: Last 15 Days Trend
last_15_days = data.tail(15)
fig_15d = px.line(
    last_15_days,
    x=last_15_days.index,
    y='Gold Price (8g)',
    title="📅 Gold Price - Last 15 Days (8g)",
    markers=True,
)
st.plotly_chart(fig_15d, use_container_width=True)

# Chart 2: Moving Average (8g)
data['Moving Avg (8g)'] = data['Gold Price (8g)'].rolling(window=7).mean()
fig_ma = px.line(
    data.tail(60),
    x=data.tail(60).index,
    y=['Gold Price (8g)', 'Moving Avg (8g)'],
    title="📊 7-Day Moving Average (8g)",
)
st.plotly_chart(fig_ma, use_container_width=True)

# Chart 3: Monthly Change
last_month = data.tail(30)
fig_month = px.bar(
    last_month,
    x=last_month.index,
    y='Gold Price (8g)',
    title="📆 Gold Price - Last 1 Month (8g)",
)
st.plotly_chart(fig_month, use_container_width=True)

# Chart 4: Yearly Average
data['Year'] = data.index.year
yearly_avg = data.groupby('Year')['Gold Price (8g)'].mean().reset_index()
fig_year = px.line(
    yearly_avg,
    x='Year',
    y='Gold Price (8g)',
    title="🗓️ Average Gold Price per Year (8g)",
    markers=True,
)
st.plotly_chart(fig_year, use_container_width=True)

# -------------------------------
# 🔮 FORECASTING NEXT 15 DAYS
# -------------------------------
st.subheader("🔮 Forecast: Next 15 Days (8 Grams)")

# Prepare data for linear regression
data = data.reset_index()
data['Day'] = np.arange(len(data))
X = data[['Day']]
y = data['Gold Price (8g)']

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict next 15 days
future_days = np.arange(len(data), len(data) + 15)
predicted_prices = model.predict(future_days.reshape(-1, 1))

# Create forecast DataFrame
future_dates = pd.date_range(start=data['Date'].iloc[-1] + timedelta(days=1), periods=15)
forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Gold Price (8g)': predicted_prices})

# Combine with actual
combined = pd.concat([data[['Date', 'Gold Price (8g)']], forecast_df.rename(columns={'Predicted Gold Price (8g)': 'Gold Price (8g)'})])

# Plot forecast chart
fig_forecast = px.line(
    combined,
    x='Date',
    y='Gold Price (8g)',
    title="📈 Forecasted Gold Price - Next 15 Days (8g)",
    markers=True,
)
fig_forecast.add_scatter(
    x=forecast_df['Date'],
    y=forecast_df['Predicted Gold Price (8g)'],
    mode='markers+lines',
    name='Predicted',
)
st.plotly_chart(fig_forecast, use_container_width=True)

# -------------------------------
# 📋 FOOTNOTE
# -------------------------------
st.caption("⚠️ Note: Prices are based on Yahoo Finance data. Forecasts are for trend estimation, not financial advice.")
