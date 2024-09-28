import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import date, timedelta

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
        # 1. Line Chart of Closing Prices
        st.subheader('Closing Price Over Time')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df['Close'], label='Close Price')
        ax.set_title(f'{stock_symbol} Stock Price Chart')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        st.pyplot(fig)

        # 2. Volume Chart
        st.subheader('Trading Volume Over Time')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df.index, df['Volume'])
        ax.set_title(f'{stock_symbol} Trading Volume')
        ax.set_xlabel('Date')
        ax.set_ylabel('Volume')
        st.pyplot(fig)

        # 3. Candlestick Chart with Moving Averages
        st.subheader('Candlestick Chart with Moving Averages')
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()

        fig, ax = mpf.plot(df, type='candle', style='yahoo',
                           title=f'{stock_symbol} Candlestick Chart',
                           ylabel='Price',
                           ylabel_lower='Volume',
                           volume=True,
                           mav=(20, 50),
                           figsize=(10, 8),
                           returnfig=True)
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
            'Average Close': df['Close'].mean(),
            '20-Day MA': df['MA20'].iloc[-1],
            '50-Day MA': df['MA50'].iloc[-1]
        }, index=['Latest Data'])
        st.write(stats.T)

        # Display recent stock data
        st.subheader('Recent Stock Data')
        st.write(df.tail())

st.sidebar.markdown("""
## About this Enhanced App

This app fetches stock price data for a specified stock and displays multiple visualizations along with basic statistical information.

Visualizations:
1. Closing Price Line Chart
2. Trading Volume Bar Chart
3. Candlestick Chart with 20 and 50-day Moving Averages

How to use:
1. Enter a stock symbol (e.g., AAPL for Apple)
2. Select the start and end dates for the analysis period
3. Click the 'Fetch Data' button

Data is retrieved from Yahoo Finance.
""")
