from core.database import Database
from config import DATA_DIR
import uuid


class ProductManager:

    def __init__(self):

        self.db = Database(DATA_DIR / "products.json")

    def all(self):
        return self.db.load()

    def create(self, name, brand, model):

        products = self.db.load()

        product = {

            "id": str(uuid.uuid4()),
            "name": name,
            "brand": brand,
            "model": model,
            "barcode": "",
            "stock_min": 1
        }

        products.append(product)

        self.db.save(products)

        return product