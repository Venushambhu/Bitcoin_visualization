# app.py - Streamlit Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv(r"C:\Users\Venu Shambhu\Desktop\DV_Project\Data\coin_Bitcoin.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df['daily_return'] = df['Close'].pct_change()
df['rolling_volatility'] = df['daily_return'].rolling(window=30).std()

# Sidebar
st.sidebar.title("Bitcoin Dashboard")
start_date = st.sidebar.date_input("Start date", df['Date'].min())
end_date = st.sidebar.date_input("End date", df['Date'].max())

# Filter by date
df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# Title
st.title("Bitcoin Price Analysis")

# Line Chart
st.subheader("Closing Price Over Time")
st.plotly_chart(px.line(df_filtered, x='Date', y='Close', title='Closing Price'))

# Daily Return Histogram
st.subheader("Distribution of Daily Returns")
st.plotly_chart(px.histogram(df_filtered.dropna(), x='daily_return', nbins=50))

# Volatility
st.subheader("30-Day Rolling Volatility")
st.line_chart(df_filtered[['Date', 'rolling_volatility']].set_index('Date'))

# Volume Chart
st.subheader("Trading Volume Over Time")
st.area_chart(df_filtered[['Date', 'Volume']].set_index('Date'))

# Summary Stats
with st.expander("📊 Summary Statistics"):
    st.write(df_filtered.describe())
