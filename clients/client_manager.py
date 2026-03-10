from core.database import db


class ClientManager:

    def all(self):
        return db.fetchall(
            "SELECT * FROM clients ORDER BY name"
        )

    def create(self, name, phone="", notes=""):
        db.execute(
            "INSERT INTO clients (name, phone, notes) VALUES (?, ?, ?)",
            (name, phone, notes)
        )

    def delete(self, client_id):
        db.execute(
            "DELETE FROM clients WHERE id=?",
            (client_id,)
        )

    def update_reputation(self, client_id, reputation):
        db.execute(
            "UPDATE clients SET reputation=? WHERE id=?",
            (reputation, client_id)
        )