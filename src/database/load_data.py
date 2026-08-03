import sqlite3

from pathlib import Path

from src.api.coingecko_api import (
    get_bitcoin_history
)


ROOT_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    ROOT_DIR
    / "data"
    / "crypto.db"
)


def create_database():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    sql_file = (
        ROOT_DIR
        / "sql"
        / "create_tables.sql"
    )

    with open(
        sql_file,
        "r",
        encoding="utf-8"
    ) as file:

        connection.executescript(
            file.read()
        )

    connection.commit()
    connection.close()


def load_market_data():

    df = get_bitcoin_history()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    df.to_sql(
        "crypto_market",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(
        f"{len(df)} records loaded."
    )