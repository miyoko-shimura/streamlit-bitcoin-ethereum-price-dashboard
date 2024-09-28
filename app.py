import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

# Set the style for the plots
plt.style.use('seaborn')

st.title('Enhanced Stock Analysis App')

# Stock symbol input
stock_symbol = st.text_input('Enter a stock symbol (e.g., AAPL for Apple):', 'AAPL')

# Date range selection
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start date', date.today() - timedelta(days=365))
with col2:
    end_date = st.date_input('End date', date.today())

if st.button('Fetch Data'):
    # Fetch stock data using yfinance
    stock_data = yf.Ticker(stock_symbol)
    df = stock_data.history(start=start_date, end=end_date)

    if df.empty:
        st.error('Unable to fetch data. Please check the stock symbol.')
    else:
        # 1. Closing Price Chart
        st.subheader('Closing Price Over Time')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df['Close'], linewidth=2, color='#1f77b4')
        ax.fill_between(df.index, df['Close'], alpha=0.1, color='#1f77b4')
        ax.set_title(f'{stock_symbol} Stock Price', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=10)
        fig.tight_layout()
        st.pyplot(fig)

        # 2. Daily Percentage Change Chart
        st.subheader('Daily Percentage Change')
        df['Daily Return'] = df['Close'].pct_change() * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(df.index, df['Daily Return'], color=['g' if x >= 0 else 'r' for x in df['Daily Return']], alpha=0.7)
        ax.set_title(f'{stock_symbol} Daily Percentage Change', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Percentage Change (%)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=10)
        fig.tight_layout()
        st.pyplot(fig)

        # 3. Volume Chart
        st.subheader('Trading Volume Over Time')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(df.index, df['Volume'], color='#2ca02c', alpha=0.7)
        ax.set_title(f'{stock_symbol} Trading Volume', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Volume', fontsize=12)
        ax.grid(
