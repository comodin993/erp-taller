from core.database import db
from inventory.piece_manager import PieceManager


class PurchaseManager:

    def __init__(self):
        self.pieces = PieceManager()

    def add(self, product_id, quantity):

        db.execute(
            "INSERT INTO purchases (product_id, quantity) VALUES (?, ?)",
            (product_id, quantity)
        )

        for _ in range(quantity):
            self.pieces.add(product_id)

    def all(self):

        return db.fetchall(
            "SELECT * FROM purchases ORDER BY id DESC"
        )