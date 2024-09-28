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
        # Simplified Closing Price Chart
        st.subheader(f'{stock_symbol} Stock Price Chart')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df['Close'], color='#1f77b4', linewidth=2)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Set labels and title
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        
        # Adjust tick parameters
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        # Add light grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # Use tight layout
        fig.tight_layout()
        
        st.pyplot(fig)

        # Basic statistics
        st.subheader('Basic Statistics')
        stats = {
            'Latest Close': f"${df['Close'].iloc[-1]:.2f}",
            'Period High': f"${df['High'].max():.2f}",
            'Period Low': f"${df['Low'].min():.2f}",
            'Average Close': f"${df['Close'].mean():.2f}",
        }
        
        # Display statistics
        col1, col2 = st.columns(2)
        for i, (key, value) in enumerate(stats.items()):
            if i % 2 == 0:
                col1.metric(key, value)
            else:
                col2.metric(key, value)

st.sidebar.markdown("""
## About this App

This app fetches stock price data and displays a simple chart of the closing price over time. It also shows some basic statistics about the stock's performance.

How to use:
1. Enter a stock symbol (e.g., AAPL for Apple)
2. Select the start and end dates
3. Click 'Fetch Data'

Data is retrieved from Yahoo Finance.
""")
