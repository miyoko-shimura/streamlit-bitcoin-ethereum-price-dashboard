import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

st.title('株価分析アプリ')

# 株式シンボルの入力
stock_symbol = st.text_input('株式シンボルを入力してください（例：7203.T for Toyota）:', '7203.T')

# 日付範囲の選択
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('開始日', date.today() - timedelta(days=365))
with col2:
    end_date = st.date_input('終了日', date.today())

if st.button('データを取得'):
    # yfinanceを使用して株価データを取得
    stock_data = yf.Ticker(stock_symbol)
    df = stock_data.history(start=start_date, end=end_date)

    if df.empty:
        st.error('データを取得できませんでした。株式シンボルを確認してください。')
    else:
        # 株価チャートの作成
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='株価'))
        fig.update_layout(title=f'{stock_symbol}の株価チャート',
                          xaxis_title='日付',
                          yaxis_title='価格')
        st.plotly_chart(fig)

        # 基本的な統計情報
        st.subheader('基本統計')
        stats = pd.DataFrame({
            '始値': df['Open'].iloc[-1],
            '高値': df['High'].iloc[-1],
            '安値': df['Low'].iloc[-1],
            '終値': df['Close'].iloc[-1],
            '出来高': df['Volume'].iloc[-1],
            '期間最高値': df['High'].max(),
            '期間最安値': df['Low'].min(),
            '平均終値': df['Close'].mean()
        }, index=['最新のデータ'])
        st.write(stats.T)

        # 株価データの表示
        st.subheader('株価データ')
        st.write(df)

st.sidebar.markdown("""
## このアプリについて

このアプリは、指定された株式の株価データを取得し、ローソク足チャートと基本的な統計情報を表示します。

使用方法:
1. 株式シンボルを入力します（日本株の場合、シンボルの後に .T を付けます）
2. 分析したい期間の開始日と終了日を選択します
3. 「データを取得」ボタンをクリックします

データはYahoo Financeから取得されます。
""")
