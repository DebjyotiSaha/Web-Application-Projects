import streamlit as st 
import yfinance as yf 
import pandas as pd 
import cufflinks as cf 
import datetime 

st.markdown("""
    Stock Price Analysis
    Shown are the stock prices of S&P 500
    """)

st.sidebar.subheader("Parameters")
start_date=st.sidebar.date_input("Start date", datetime.date(2010, 1, 1))
end_date=st.sidebar.date_input("End date", datetime.date(2021, 2, 28))

ticker_list=pd.read_csv("E:\Projects\Combined Projects\constituents_symbols.txt")
tickerSymbol=st.sidebar.selectbox('Stock ticker', ticker_list)
tickerData=yf.Ticker(tickerSymbol)
tickerDf=tickerData.history(period='1d', start=start_date, end=end_date)

string_logo='<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name=tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary=tickerData.info['longBusinessSummary']
st.info(string_summary)

st.header("**Prices Range**")
st.write(tickerDf)

st.header("**Bands**")
qf=cf.QuantFig(tickerDf, title='Chart', legend='top', name='GS')
qf.add_bollinger_bands()
fig=qf.iplot(asFigure=True)
st.plotly_chart(fig)