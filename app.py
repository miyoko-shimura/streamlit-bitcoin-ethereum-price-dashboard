import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.title('Simple Stock Analysis App')

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
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df['Close'])
        ax.set_title(f'{stock_symbol} Stock Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        st.pyplot(fig)

        # 2. Daily Percentage Change Chart
        st.subheader('Daily Percentage Change')
        df['Daily Return'] = df['Close'].pct_change() * 100
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df.index, df['Daily Return'])
        ax.set_title(f'{stock_symbol} Daily Percentage Change')
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage Change')
        st.pyplot(fig)

        # 3. Volume Chart
        st.subheader('Trading Volume Over Time')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df.index, df['Volume'])
        ax.set_title(f'{stock_symbol} Trading Volume')
        ax.set_xlabel('Date')
        ax.set_ylabel('Volume')
        st.pyplot(fig)

        # Basic statistics
        st.subheader('Basic Statistics')
        stats = pd.DataFrame({
            'Latest Close': df['Close'].iloc[-1],
            'Period High': df['High'].max(),
            'Period Low': df['Low'].min(),
            'Average Close': df['Close'].mean(),
            'Total Volume': df['Volume'].sum(),
            'Average Daily Return': df['Daily Return'].mean(),
            'Return Volatility': df['Daily Return'].std()
        }, index=['Value'])
        st.write(stats.T)

st.sidebar.markdown("""
## About this App

This app fetches stock price data and displays three simple charts:

1. Closing Price Over Time
2. Daily Percentage Change
3. Trading Volume Over Time

It also shows some basic statistics about the stock's performance.

How to use:
1. Enter a stock symbol (e.g., AAPL for Apple)
2. Select the start and end dates
3. Click 'Fetch Data'

Data is retrieved from Yahoo Finance.
""")
