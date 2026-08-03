from src.database.load_data import (
    create_database,
    load_market_data
)

from src.processing.preprocess_data import (
    build_dataset
)

from src.models.train_model import (
    train_models
)


def main():

    print(
        "Creating database..."
    )

    create_database()

    print(
        "Loading Bitcoin historical data..."
    )

    load_market_data()

    print(
        "Building ML dataset..."
    )

    build_dataset()

    print(
        "Training models..."
    )

    train_models()

    print(
        "Completed."
    )


if __name__ == "__main__":
    main()