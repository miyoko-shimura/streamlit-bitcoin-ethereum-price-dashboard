import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.title('Stock Analysis App')

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
        # Create stock price chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df['Close'], label='Close Price')
        ax.set_title(f'{stock_symbol} Stock Price Chart')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        st.pyplot(fig)

        # Basic statistics
        st.subheader('Basic Statistics')
        stats = pd.DataFrame({
            'Open': df['Open'].iloc[-1],
            'High': df['High'].iloc[-1],
            'Low': df['Low'].iloc[-1],
            'Close': df['Close'].iloc[-1],
            'Volume': df['Volume'].iloc[-1],
            'Period High': df['High'].max(),
            'Period Low': df['Low'].min(),
            'Average Close': df['Close'].mean()
        }, index=['Latest Data'])
        st.write(stats.T)

        # Display stock data
        st.subheader('Stock Data')
        st.write(df)

st.sidebar.markdown("""
## About this App

This app fetches stock price data for a specified stock and displays a price chart along with basic statistical information.

How to use:
1. Enter a stock symbol (e.g., AAPL for Apple)
2. Select the start and end dates for the analysis period
3. Click the 'Fetch Data' button

Data is retrieved from Yahoo Finance.
""")
