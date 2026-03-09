from core.database import Database
from config import DATA_DIR


class PurchaseManager:

    def __init__(self):

        self.db = Database(DATA_DIR / "purchases.json")

    def all(self):

        return self.db.load()

    def add(self, product_id, qty=1):

        data = self.db.load()

        for item in data:

            if item["product_id"] == product_id:

                item["qty"] += qty

                self.db.save(data)

                return

        data.append({

            "product_id": product_id,
            "qty": qty

        })

        self.db.save(data)