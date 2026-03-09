from core.database import Database
from config import DATA_DIR


class LocationManager:

    def __init__(self):

        self.db = Database(DATA_DIR / "locations.json")

    def all(self):

        return self.db.load()

    def add(self, name):

        data = self.db.load()

        data.append(name)

        self.db.save(data)