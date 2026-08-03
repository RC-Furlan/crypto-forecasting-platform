from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "dataset_model.csv"
)

df = pd.read_csv(DATASET_PATH)

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

df["daily_return"] = (
    df["price"]
    .pct_change()
    * 100
)

st.set_page_config(
    layout="wide"
)

st.title(
    "Market Analysis"
)

st.subheader(
    "Price Analysis"
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["price"],
        name="Price"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["ma30"],
        name="MA 30"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["ma90"],
        name="MA 90"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

left, right = st.columns(2)

with left:

    fig_hist = px.histogram(
        df,
        x="daily_return",
        nbins=40,
        title="Daily Return Distribution"
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

with right:

    corr = df[
        [
            "price",
            "market_cap",
            "volume"
        ]
    ].corr()

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

st.divider()

fig_scatter = px.scatter(
    df,
    x="volume",
    y="price",
    title="Volume vs Price"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)