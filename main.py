from datetime import datetime
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.graph_objs as go

# st.set_page_config(layout="wide")
exact_time = datetime.utcnow()
count = st_autorefresh(interval=2000)

st.title("Crypto Currency Price Tracker")
st.subheader(
    "This application tracks the live prices of Bitcoin, Dogecoin, and Ethereum. It is refreshed every 2 seconds.")
st.caption("Created by Your Name")

price_key = "https://api.binance.com/api/v3/ticker/price?symbol="
crypto_types = {"Bitcoin": "BTCUSDT", "Dogecoin": "DOGEUSDT", "Ethereum": "ETHUSDT"}

crypto_selection = st.selectbox("View price of a specific coin", crypto_types)


def get_price_data(coin):
    url = price_key + crypto_types[coin]
    data = requests.get(url)
    data = data.json()
    return data


coin_data = get_price_data(crypto_selection)

coin_price = coin_data["price"]
coin_price_rounded = str(round(float(coin_price), 5))

st.write(f"**TIME**: {exact_time} UTC")
st.write(f"The current price of {crypto_selection} is **${coin_price_rounded}**")

# Getting graph data
candle_stick_key = "https://api.binance.com/api/v3/klines?symbol=" + crypto_types[crypto_selection] + "&interval=1m"
candle_stick_data = requests.get(candle_stick_key)
candle_stick_data = candle_stick_data.json()

# Create pandas DataFrame of graph data
df = pd.DataFrame(candle_stick_data)
df = df.iloc[:, :5]

df.columns = ["Time", "Open", "High", "Low", "Close"]
df["Time"] = pd.to_datetime(df["Time"], unit="ms")
print(df["Time"])

# Create graph
fig = go.Figure()

fig.add_trace(go.Candlestick(x=df["Time"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"]))
fig.update_layout(title=f"{crypto_selection}", yaxis_title=f"{crypto_selection} Price in Dollars")

st.plotly_chart(fig, use_container_width=True)
