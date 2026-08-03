from pathlib import Path

import pandas as pd
import sqlite3


ROOT_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    ROOT_DIR
    / "data"
    / "crypto.db"
)

OUTPUT_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "dataset_model.csv"
)


def build_dataset():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    query = """
    SELECT *
    FROM crypto_market
    ORDER BY date
    """

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month

    df["day"] = df["date"].dt.day

    df["day_of_week"] = (
        df["date"]
        .dt.dayofweek
    )

    df["week_of_year"] = (
        df["date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["lag_1"] = (
        df["price"]
        .shift(1)
    )

    df["lag_7"] = (
        df["price"]
        .shift(7)
    )

    df["lag_14"] = (
        df["price"]
        .shift(14)
    )

    df["lag_30"] = (
        df["price"]
        .shift(30)
    )

    df["rolling_mean_7"] = (
        df["price"]
        .rolling(7)
        .mean()
    )

    df["rolling_mean_30"] = (
        df["price"]
        .rolling(30)
        .mean()
    )

    df["rolling_mean_90"] = (
        df["price"]
        .rolling(90)
        .mean()
    )

    df = df.dropna()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"{len(df)} rows exported."
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )