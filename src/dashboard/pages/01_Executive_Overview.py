from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "dataset_model.csv"
)

MODEL_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "model_comparison.csv"
)

st.set_page_config(
    layout="wide"
)

st.markdown(
    """
    <style>

    .block-container{
        padding-top:1rem;
    }

    div[data-testid="metric-container"]{
        border:1px solid #262730;
        padding:15px;
        border-radius:10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv(DATASET_PATH)

models = pd.read_csv(MODEL_PATH)

df["date"] = pd.to_datetime(df["date"])

df["ma30"] = (
    df["price"]
    .rolling(30)
    .mean()
)

df["ma90"] = (
    df["price"]
    .rolling(90)
    .mean()
)

current_price = df["price"].iloc[-1]

return_30d = (
    (
        current_price
        - df["price"].iloc[-30]
    )
    /
    df["price"].iloc[-30]
) * 100

return_90d = (
    (
        current_price
        - df["price"].iloc[-90]
    )
    /
    df["price"].iloc[-90]
) * 100

volatility = (
    df["price"]
    .pct_change()
    .std()
    * (365 ** 0.5)
    * 100
)

market_cap = df["market_cap"].iloc[-1]

best_r2 = models["R2"].max()

st.title(
    "Executive Overview"
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Current Price",
    f"${current_price:,.0f}"
)

c2.metric(
    "30D Return",
    f"{return_30d:.2f}%"
)

c3.metric(
    "90D Return",
    f"{return_90d:.2f}%"
)

c4.metric(
    "Volatility",
    f"{volatility:.2f}%"
)

c5.metric(
    "Market Cap",
    f"${market_cap/1e12:.2f}T"
)

c6.metric(
    "Best R²",
    f"{best_r2:.3f}"
)

st.divider()

st.subheader(
    "Price Trend with Moving Averages"
)

fig = px.line(
    df,
    x="date",
    y=[
        "price",
        "ma30",
        "ma90"
    ]
)

fig.update_traces(
    line=dict(width=3)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader(
    "Market Summary"
)

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Highest Price",
    f"${df['price'].max():,.0f}"
)

s2.metric(
    "Lowest Price",
    f"${df['price'].min():,.0f}"
)

s3.metric(
    "Average Volume",
    f"${df['volume'].mean()/1e9:.2f}B"
)

s4.metric(
    "Dataset Size",
    f"{len(df)}"
)