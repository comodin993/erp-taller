from core.database import db


class PieceManager:

    def add(self, product_id, note=""):
        db.execute(
            "INSERT INTO pieces (product_id, note) VALUES (?, ?)",
            (product_id, note)
        )

    def count_by_product(self, product_id):
        row = db.fetchone(
            "SELECT COUNT(*) as total FROM pieces WHERE product_id = ?",
            (product_id,)
        )

        if row:
            return row["total"]

        return 0

    def all(self):
        return db.fetchall(
            "SELECT * FROM pieces ORDER BY id DESC"
        )