import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# Set the page title and header
st.set_page_config(page_title="Bitcoin Price", page_icon=":moneybag:")
st.title("Bitcoin Price Dashboard")

# Define the Bitcoin ticker symbol
bitcoin_symbol = "BTC-USD"

# Fetch the historical Bitcoin price data
bitcoin_data = yf.download(bitcoin_symbol, period="1y", interval="1d")

if len(bitcoin_data) > 0:
    current_price = bitcoin_data["Close"][-1]
    st.metric(label="Current Bitcoin Price (USD)", value=f"${current_price:.2f}")

    # Plot the historical price data
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(bitcoin_data["Close"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (USD)")
    ax.set_title("Bitcoin Price History (1 Year)")
    ax.grid()
    st.pyplot(fig)

    # Display data in a table
    st.subheader("Historical Price Data")
    st.write(bitcoin_data)
else:
    st.warning("Failed to fetch Bitcoin price data.")
