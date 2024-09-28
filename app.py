import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_price(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Close']

def plot_stock_price(prices, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(prices.index, prices.values)
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    return plt

st.title('Simple Stock Price App')

ticker = st.text_input('Enter a stock ticker (e.g., AAPL, GOOGL):', 'AAPL')
start_date = st.date_input('Start date')
end_date = st.date_input('End date')

if st.button('Show Stock Price'):
    prices = get_stock_price(ticker, start_date, end_date)
    fig = plot_stock_price(prices, ticker)
    st.pyplot(fig)
