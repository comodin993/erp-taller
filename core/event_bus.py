import json
from pathlib import Path

class Database:

    def __init__(self, path):
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf8")

    def load(self):
        with open(self.path, "r", encoding="utf8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)