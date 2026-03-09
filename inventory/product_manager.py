from core.database import Database
from config import DATA_DIR
import uuid


class ProductManager:

    def __init__(self):
        self.db = Database(DATA_DIR / "products.json")

    def all(self):
        return self.db.load()

    def create(self, name, brand, model, stock_min=1):

        products = self.db.load()

        product = {

            "id": str(uuid.uuid4()),
            "name": name,
            "brand": brand,
            "model": model,
            "barcode": "",
            "stock_min": stock_min,
            "price": 0

        }

        products.append(product)

        self.db.save(products)

        return product

    def get(self, product_id):

        products = self.db.load()

        for p in products:

            if p["id"] == product_id:

                return p