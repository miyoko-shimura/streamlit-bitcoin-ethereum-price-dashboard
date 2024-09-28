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
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=10)
        fig.tight_layout()
        st.pyplot(fig)

        # Improved Basic statistics display
        st.subheader('Basic Statistics')
        
        # Prepare the statistics
        stats = {
            'Latest Close': f"${df['Close'].iloc[-1]:.2f}",
            'Period High': f"${df['High'].max():.2f}",
            'Period Low': f"${df['Low'].min():.2f}",
            'Average Close': f"${df['Close'].mean():.2f}",
            'Total Volume': f"{df['Volume'].sum():,.0f}",
            'Average Daily Return': f"{df['Daily Return'].mean():.2f}%",
            'Return Volatility': f"{df['Daily Return'].std():.2f}%"
        }
        
        # Create two columns for a more compact display
        col1, col2 = st.columns(2)
        
        # Display the statistics in two columns
        for i, (key, value) in enumerate(stats.items()):
            if i % 2 == 0:
                col1.metric(key, value)
            else:
                col2.metric(key, value)

st.sidebar.markdown("""
## About this App

This app fetches stock price data and displays three informative charts:

1. Closing Price Over Time
2. Daily Percentage Change
3. Trading Volume Over Time

It also shows key statistics about the stock's performance.

How to use:
1. Enter a stock symbol (e.g., AAPL for Apple)
2. Select the start and end dates
3. Click 'Fetch Data'

Data is retrieved from Yahoo Finance.
""")
