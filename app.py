import yfinance as yf
import streamlit as st

# Set the page title and header
st.set_page_config(page_title="Bitcoin Price", page_icon=":moneybag:")
st.title("Current Bitcoin Price")

# Define the Bitcoin ticker symbol
bitcoin_symbol = "BTC-USD"

# Fetch the current Bitcoin price
bitcoin_data = yf.download(bitcoin_symbol, period="1d", interval="1m")

if len(bitcoin_data) > 0:
    current_price = bitcoin_data["Close"][-1]
    st.metric(label="Bitcoin Price (USD)", value=f"${current_price:.2f}")
else:
    st.warning("Failed to fetch the current Bitcoin price.")
