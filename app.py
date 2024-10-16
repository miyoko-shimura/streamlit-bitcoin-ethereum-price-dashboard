import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set the page title and header
st.set_page_config(page_title="BTC and ETH Prices", page_icon=":moneybag:")
st.title("Bitcoin and Ethereum Price Dashboard")

# Define the list of cryptocurrency symbols
crypto_symbols = ["BTC-USD", "ETH-USD"]

# Create a dropdown to select the cryptocurrency
selected_symbol = st.selectbox("Select Cryptocurrency", crypto_symbols)

# Define the period options and their corresponding timedelta
period_options = {
    "Last 1 Month": timedelta(days=30),
    "Last 3 Months": timedelta(days=90),
    "Last 6 Months": timedelta(days=180),
    "Last 1 Year": timedelta(days=365),
    "Last 2 Years": timedelta(days=365*2),
    "Last 3 Years": timedelta(days=365*3),
    "Last 5 Years": timedelta(days=365*5),
    "Last 10 Years": timedelta(days=365*10)
}

# Create a dropdown to select the period
selected_period = st.selectbox("Select Period", list(period_options.keys()))

# Set the end date to the current date and calculate the start date based on the selected period
end_date = datetime.now().date()
start_date = end_date - period_options[selected_period]

# Create a date range slider
date_range = st.slider(
    "Select Date Range",
    value=(start_date, end_date),
    format="YYYY-MM-DD"
)
start_date = date_range[0]
end_date = date_range[1]

# Fetch the latest price data
ticker = yf.Ticker(selected_symbol)
latest_data = ticker.history(period="1d")

if not latest_data.empty:
    current_price = latest_data["Close"].iloc[-1]
    st.metric(label=f"Latest {selected_symbol} Price (USD)", value=f"${current_price:.2f}")

    # Fetch the historical price data for the selected cryptocurrency and date range
    crypto_data = yf.download(selected_symbol, start=start_date, end=end_date, interval="1d")

    if len(crypto_data) > 0:
        # Plot the historical price data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(crypto_data["Close"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price (USD)")
        ax.set_title(f"{selected_symbol} Price History ({start_date} to {end_date})")
        
        # Remove the frame
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        st.pyplot(fig)

        # Display data in a table
        st.subheader("Historical Price Data")
        st.write(crypto_data)
    else:
        st.warning(f"Failed to fetch historical {selected_symbol} price data.")
else:
    st.warning(f"Failed to fetch latest {selected_symbol} price data.")
