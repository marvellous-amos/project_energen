from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

TRAIN_START = "2014-11-01 00:00:00"
TEST_START = "2014-12-30 00:00:00"

SEASONAL_PERIOD = 24
HORIZON = 3
