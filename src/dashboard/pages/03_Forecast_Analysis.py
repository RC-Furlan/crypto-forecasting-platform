from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]

PREDICTIONS_PATH = (
    ROOT_DIR
    / "data"
    / "predictions"
    / "predictions.csv"
)

MODEL_RESULTS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "model_comparison.csv"
)

predictions = pd.read_csv(
    PREDICTIONS_PATH
)

results = pd.read_csv(
    MODEL_RESULTS_PATH
)

st.set_page_config(
    page_title="Forecast Analysis",
    layout="wide"
)

st.markdown(
    """
    <style>

    .block-container{
        max-width:1400px;
        padding-top:1rem;
    }

    div[data-testid="metric-container"]{
        border:1px solid #2b2b2b;
        border-radius:12px;
        padding:15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title(
    "Forecast Analysis"
)

best_model = (
    results
    .sort_values(
        "R2",
        ascending=False
    )
    .iloc[0]
)

r2 = best_model["R2"]
mae = best_model["MAE"]
rmse = best_model["RMSE"]

predictions["Error"] = (
    predictions["Actual"]
    - predictions["Predicted"]
)

predictions["Absolute Error"] = (
    predictions["Error"]
    .abs()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Best Model",
    best_model["Model"]
)

c2.metric(
    "R²",
    f"{r2:.3f}"
)

c3.metric(
    "MAE",
    f"{mae:.2f}"
)

c4.metric(
    "RMSE",
    f"{rmse:.2f}"
)

st.divider()

st.subheader(
    "Model Comparison"
)

st.dataframe(
    results,
    use_container_width=True
)

st.divider()

st.subheader(
    "Actual vs Predicted"
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=predictions["Actual"],
        name="Actual",
        line=dict(
            color="#1f77b4",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatter(
        y=predictions["Predicted"],
        name="Predicted",
        line=dict(
            color="#ff4b4b",
            width=3
        )
    )
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

left, right = st.columns(2)

with left:

    fig_error = px.line(
        predictions,
        y="Absolute Error",
        title="Prediction Error Over Time"
    )

    fig_error.update_traces(
        line=dict(
            color="#ff7f0e",
            width=3
        )
    )

    st.plotly_chart(
        fig_error,
        use_container_width=True
    )

with right:

    fig_distribution = px.histogram(
        predictions,
        x="Error",
        nbins=30,
        title="Prediction Error Distribution"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )

st.divider()

st.subheader(
    "Prediction Dataset"
)

st.dataframe(
    predictions.tail(20),
    use_container_width=True
)

st.download_button(
    label="Download Predictions CSV",
    data=predictions.to_csv(index=False),
    file_name="predictions.csv",
    mime="text/csv"
)