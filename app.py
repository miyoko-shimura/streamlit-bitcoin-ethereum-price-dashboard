import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import mplfinance as mpf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")
    return history

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def plot_stock_data(data):
    # Create subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16), sharex=True)
    
    # Plot candlestick chart
    mpf.plot(data, type='candle', ax=ax1, volume=False, style='yahoo')
    ax1.set_title('Stock Price')
    ax1.set_ylabel('Price')
    
    # Plot RSI
    ax2.plot(data.index, data['RSI'], label='RSI')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_title('RSI')
    ax2.set_ylabel('RSI')
    ax2.legend()
    
    # Plot MACD
    ax3.plot(data.index, data['MACD'], label='MACD')
    ax3.plot(data.index, data['Signal'], label='Signal')
    ax3.bar(data.index, data['Histogram'], label='Histogram')
    ax3.set_title('MACD')
    ax3.set_ylabel('MACD')
    ax3.legend()
    
    # Format x-axis
    date_formatter = DateFormatter("%Y-%m-%d")
    ax3.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()
    
    plt.tight_layout()
    return fig

def main():
    st.title("株価表示アプリ（テクニカル指標付き）")

    ticker = st.text_input("株式のティッカーシンボルを入力してください（例：AAPL, GOOGL）:")
    
    if ticker:
        data = get_stock_price(ticker)
        
        if not data.empty:
            st.subheader(f"{ticker}の株価推移とテクニカル指標（過去1年間）")
            
            # Calculate technical indicators
            data['RSI'] = calculate_rsi(data)
            data['MACD'], data['Signal'], data['Histogram'] = calculate_macd(data)
            
            # Plot the data
            fig = plot_stock_data(data)
            st.pyplot(fig)
            
            st.subheader("データ統計")
            st.write(data['Close'].describe())
        else:
            st.error("データを取得できませんでした。ティッカーシンボルが正しいか確認してください。")

if __name__ == "__main__":
    main()
