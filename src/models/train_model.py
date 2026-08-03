from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split

from xgboost import XGBRegressor


ROOT_DIR = Path(__file__).resolve().parents[2]

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
    / "best_model.pkl"
)

COMPARISON_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "model_comparison.csv"
)

PREDICTIONS_PATH = (
    ROOT_DIR
    / "data"
    / "predictions"
    / "predictions.csv"
)


def train_models():

    df = pd.read_csv(
        DATASET_PATH
    )

    X = df.drop(
        columns=[
            "date",
            "price"
        ]
    )

    y = df["price"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False
        )
    )

    models = {

        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42
        ),

        "XGBoost": XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )
    }

    results = []

    best_model = None
    best_score = float("-inf")
    best_predictions = None

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = (
            mean_squared_error(
                y_test,
                predictions
            ) ** 0.5
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        results.append(
            {
                "Model": name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2
            }
        )

        if r2 > best_score:

            best_score = r2

            best_model = model

            best_predictions = predictions

    comparison = pd.DataFrame(
        results
    )

    comparison.to_csv(
        COMPARISON_PATH,
        index=False
    )

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    PREDICTIONS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    prediction_df = pd.DataFrame(
        {
            "Actual": y_test.values,
            "Predicted": best_predictions
        }
    )

    prediction_df.to_csv(
        PREDICTIONS_PATH,
        index=False
    )

    print(
        comparison
    )

    print(
        f"\nPredictions saved: {PREDICTIONS_PATH}"
    )

    print(
        "\nBest model saved."
    )