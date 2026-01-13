import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from data.polymarket import fetch_event, pick_market

st.title("Polymarket Monitor")

EVENT_ID = "16282"
MARKET_MATCH = "250,000-500,000"  # pick one contract to start

# refresh every 60s
st_autorefresh(interval=60_000, key="refresh")

event = fetch_event(EVENT_ID)
market = pick_market(event, MARKET_MATCH)

# # outcomePrices is usually ["price_yes","price_no"] as strings
# prices = [float(x) for x in market["outcomePrices"]]
# p_yes = prices[0]
import json

outcome_prices = market["outcomePrices"]

# Polymarket sometimes returns this as a JSON string like '["0.1","0.9"]'
if isinstance(outcome_prices, str):
    outcome_prices = json.loads(outcome_prices)

prices = [float(x) for x in outcome_prices]
p_yes = prices[0]


st.subheader(market["question"])
st.metric("P(Yes)", f"{p_yes:.4f}")

# keep a little time series in session_state
if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append({"t": pd.Timestamp.utcnow(), "p_yes": p_yes})
df = pd.DataFrame(st.session_state.history)

st.line_chart(df.set_index("t")["p_yes"])
st.caption(f"Last update: {pd.Timestamp.utcnow().isoformat()}Z")
