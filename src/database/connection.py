from pathlib import Path
from sqlalchemy import create_engine


ROOT_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    ROOT_DIR
    / "data"
    / "crypto.db"
)

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)