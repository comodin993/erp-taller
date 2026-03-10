from core.database import db


class ProductManager:

    def __init__(self):
        pass

    # -------------------------

    def all(self):

        return db.fetchall(
            "SELECT * FROM products ORDER BY id DESC"
        )

    # -------------------------

    def create(self, name, brand, model):

        db.execute(
            """
            INSERT INTO products (name, brand, model)
            VALUES (?, ?, ?)
            """,
            (name, brand, model)
        )

    # -------------------------

    def get(self, product_id):

        return db.fetchone(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )

    # -------------------------

    def delete(self, product_id):

        db.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )