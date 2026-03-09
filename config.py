from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "indexes"

DATA_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)