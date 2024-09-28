import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def main():
    st.title("Stock Price App with Technical Indicators")

    ticker = st.text_input("Enter a stock ticker symbol (e.g., AAPL, GOOGL):")
    
    if ticker:
        data = get_stock_price(ticker)
        
        if not data.empty:
            st.subheader(f"{ticker} Stock Price and Technical Indicators (Past Year)")
            
            # Calculate technical indicators
            data['RSI'] = calculate_rsi(data)
            data['MACD'], data['Signal'], data['Histogram'] = calculate_macd(data)
            
            # Create subplots
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                vertical_spacing=0.05, 
                                row_heights=[0.5, 0.25, 0.25])
            
            # Price chart
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                         low=data['Low'], close=data['Close'], name='Price'),
                          row=1, col=1)
            
            # RSI
            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            # MACD
            fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD'), row=3, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['Signal'], name='Signal'), row=3, col=1)
            fig.add_trace(go.Bar(x=data.index, y=data['Histogram'], name='Histogram'), row=3, col=1)
            
            fig.update_layout(height=900, title=f"{ticker} Stock Analysis", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
            
            st.subheader("Data Statistics")
            st.write(data['Close'].describe())
        else:
            st.error("Failed to fetch data. Please check if the ticker symbol is correct.")

if __name__ == "__main__":
    main()
