import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Noise Demo", layout="wide")
st.title("Live Noise Demo (auto-refresh)")

col1, col2, col3 = st.columns(3)
with col1:
    refresh_seconds = st.slider("Refresh interval (seconds)", 5, 120, 60)
with col2:
    n_points = st.slider("Points", 50, 2000, 500)
with col3:
    amplitude = st.slider("Amplitude", 0.1, 10.0, 1.0)

# Rerun the script every N seconds (no while loop needed)
st_autorefresh(interval=refresh_seconds * 1000, key="auto_refresh")

# New random series every rerun
x = np.arange(n_points)
y = amplitude * np.random.normal(size=n_points)

st.caption(f"Last update (server time): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="noise"))
fig.update_layout(
    height=500,
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis_title="t",
    yaxis_title="value",
)

st.plotly_chart(fig, use_container_width=True)
