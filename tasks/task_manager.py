from core.database import db


class TaskManager:

    def all(self):

        return db.fetchall("""
        SELECT
            tasks.id,
            clients.name as client,
            products.name as product,
            tasks.description,
            tasks.status
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        LEFT JOIN products ON tasks.product_id = products.id
        ORDER BY tasks.id DESC
        """)

    # -----------------------------

    def create(self, client_id, product_id, description):

        db.execute(
            """
            INSERT INTO tasks (client_id, product_id, description)
            VALUES (?, ?, ?)
            """,
            (client_id, product_id, description)
        )

    # -----------------------------

    def update_status(self, task_id, status):

        db.execute(
            "UPDATE tasks SET status=? WHERE id=?",
            (status, task_id)
        )

    # -----------------------------

    def delete(self, task_id):

        db.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )