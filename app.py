import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# Set the page title and header
st.set_page_config(page_title="Stock Price History", page_icon=":chart_with_upwards_trend:")
st.title("Stock Price History")

# Get the stock ticker symbol from the user
ticker_symbol = st.text_input("Enter the stock ticker symbol (e.g., AAPL, GOOGL):")

if ticker_symbol:
    # Download the stock data
    stock_data = yf.download(ticker_symbol)

    if len(stock_data) > 0:
        # Plot the closing price history
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(stock_data["Close"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price (USD)")
        ax.set_title(f"{ticker_symbol} Stock Price History")
        ax.grid()
        
        # Display the plot in the Streamlit app
        st.pyplot(fig)
    else:
        st.warning(f"No data found for the ticker symbol: {ticker_symbol}")
else:
    st.info("Please enter a stock ticker symbol to view its price history.")
