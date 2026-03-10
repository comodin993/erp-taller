from core.database import db


class TaskManager:

    # --------------------------------------

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

    # --------------------------------------

    def create(self, client_id, product_id, description):

        cursor = db.execute(
            """
            INSERT INTO tasks (client_id, product_id, description)
            VALUES (?, ?, ?)
            """,
            (client_id, product_id, description)
        )

        task_id = cursor.lastrowid

        # Crear subtareas automáticas básicas
        self.create_default_steps(task_id, product_id, description)

    # --------------------------------------

    def create_default_steps(self, task_id, product_id, description):

        desc = description.lower()

        # ejemplo simple de lógica
        if "modulo" in desc or "módulo" in desc:

            # conseguir pieza
            db.execute(
                """
                INSERT INTO task_steps
                (task_id, type, description, product_id)
                VALUES (?, 'material', 'Conseguir módulo', ?)
                """,
                (task_id, product_id)
            )

            # instalar pieza
            db.execute(
                """
                INSERT INTO task_steps
                (task_id, type, description)
                VALUES (?, 'action', 'Instalar módulo')
                """,
                (task_id,)
            )

    # --------------------------------------

    def steps(self, task_id):

        return db.fetchall(
            "SELECT * FROM task_steps WHERE task_id=?",
            (task_id,)
        )

    # --------------------------------------

    def complete_step(self, step_id):

        db.execute(
            "UPDATE task_steps SET status='done' WHERE id=?",
            (step_id,)
        )

        # verificar si el trabajo ya terminó
        self.check_task_completion(step_id)

    # --------------------------------------

    def check_task_completion(self, step_id):

        step = db.fetchone(
            "SELECT task_id FROM task_steps WHERE id=?",
            (step_id,)
        )

        if not step:
            return

        task_id = step["task_id"]

        pending = db.fetchone(
            """
            SELECT COUNT(*) as total
            FROM task_steps
            WHERE task_id=? AND status='pending'
            """,
            (task_id,)
        )

        if pending["total"] == 0:

            db.execute(
                "UPDATE tasks SET status='terminado' WHERE id=?",
                (task_id,)
            )