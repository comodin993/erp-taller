from core.database import Database
from config import DATA_DIR
import uuid


class PieceManager:

    def __init__(self):

        self.db = Database(DATA_DIR / "pieces.json")

    def all(self):

        return self.db.load()

    def create(self, product_id, location):

        pieces = self.db.load()

        piece = {

            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "location": location,
            "condition": "",
            "quality": "",
            "despiece_id": ""

        }

        pieces.append(piece)

        self.db.save(pieces)

        return piece

    def count_by_product(self, product_id):

        pieces = self.db.load()

        count = 0

        for p in pieces:

            if p["product_id"] == product_id:

                count += 1

        return count