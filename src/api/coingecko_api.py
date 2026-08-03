import os

import pandas as pd
import requests

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv(
    "COINGECKO_API_KEY"
)

BASE_URL = (
    "https://api.coingecko.com/api/v3"
)


def get_bitcoin_history():

    endpoint = (
        f"{BASE_URL}/coins/bitcoin/market_chart"
    )

    params = {
        "vs_currency": "usd",
        "days": "365"
    }

    response = requests.get(
        endpoint,
        params=params,
        headers={
            "x-cg-demo-api-key": API_KEY
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    prices = pd.DataFrame(
        data["prices"],
        columns=[
            "timestamp",
            "price"
        ]
    )

    market_caps = pd.DataFrame(
        data["market_caps"],
        columns=[
            "timestamp",
            "market_cap"
        ]
    )

    volumes = pd.DataFrame(
        data["total_volumes"],
        columns=[
            "timestamp",
            "volume"
        ]
    )

    df = (
        prices
        .merge(
            market_caps,
            on="timestamp"
        )
        .merge(
            volumes,
            on="timestamp"
        )
    )

    df["date"] = pd.to_datetime(
        df["timestamp"],
        unit="ms"
    )

    df = df[
        [
            "date",
            "price",
            "market_cap",
            "volume"
        ]
    ]

    return df