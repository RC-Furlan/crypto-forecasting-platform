from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

IMAGE_PATH = (
    ROOT_DIR
    / "imagens"
    / "crypto-forecasting-platform.jpg"
)

MODEL_RESULTS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "model_comparison.csv"
)

DATASET_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "dataset_model.csv"
)

st.set_page_config(
    page_title="Bitcoin Forecasting Platform",
    page_icon="₿",
    layout="wide"
)

st.markdown(
    """
    <style>

    .block-container{
        max-width:1400px;
        padding-top:1rem;
        padding-bottom:1rem;
    }

    div[data-testid="metric-container"]{
        border:1px solid #2b2b2b;
        border-radius:12px;
        padding:15px;
    }

    div[data-testid="stImage"]{
        margin-top:60px;
    }

    div[data-testid="stImage"] img{
        border-radius:24px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

dataset = pd.read_csv(
    DATASET_PATH
)

results = pd.read_csv(
    MODEL_RESULTS_PATH
)

best_model = (
    results
    .sort_values(
        "R2",
        ascending=False
    )
    .iloc[0]
)

current_price = dataset["price"].iloc[-1]

hero_left, hero_right = st.columns(
    [1.4, 1],
    vertical_alignment="center"
)

with hero_left:

    st.title(
        "Bitcoin Forecasting Platform"
    )

    st.markdown(
        """
        ## End-to-End Machine Learning Project

        Forecasting Bitcoin (BTC) prices using real-world market data from CoinGecko.

        This platform demonstrates a complete production-style analytics workflow:

        - CoinGecko API Integration
        - SQLite Database
        - Data Processing & Feature Engineering
        - Machine Learning Forecasting
        - Model Evaluation
        - Interactive Business Dashboard

        Historical Bitcoin market data is collected, transformed and used to train  
        predictive models capable of forecasting future price behaviour.
        """
    )

    k1, k2 = st.columns(2)

    k1.metric(
        "Current BTC Price",
        f"${current_price:,.0f}"
    )

    k2.metric(
        "Best Model R²",
        f"{best_model['R2']:.3f}"
    )

with hero_right:

    st.image(
        str(IMAGE_PATH),
        use_container_width=True
    )

st.divider()

st.subheader(
    "Project Architecture"
)

a1, a2, a3, a4, a5 = st.columns(5)

a1.info("Data Collection")
a2.info("Data Engineering")
a3.info("Machine Learning")
a4.info("Forecasting")
a5.info("Visualization")

st.divider()

st.subheader(
    "Project Highlights"
)

h1, h2, h3, h4 = st.columns(4)

h1.metric(
    "Historical Records",
    f"{len(dataset)}"
)

h2.metric(
    "Machine Learning Models",
    f"{len(results)}"
)

h3.metric(
    "Engineered Features",
    "15+"
)

h4.metric(
    "Best R²",
    f"{best_model['R2']:.3f}"
)

st.divider()

st.subheader(
    "Model Performance"
)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Best Model",
    best_model["Model"]
)

m2.metric(
    "R²",
    f"{best_model['R2']:.3f}"
)

m3.metric(
    "MAE",
    f"{best_model['MAE']:.2f}"
)

m4.metric(
    "RMSE",
    f"{best_model['RMSE']:.2f}"
)

st.divider()

st.subheader(
    "Technology Stack"
)

t1, t2, t3, t4, t5, t6, t7 = st.columns(7)

t1.success("CoinGecko")
t2.success("SQLite")
t3.success("Pandas")
t4.success("Scikit-Learn")
t5.success("XGBoost")
t6.success("Plotly")
t7.success("Streamlit")