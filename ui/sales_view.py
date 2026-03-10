from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QGroupBox
)

from core.database import db


class SalesView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Trabajos terminados / Entregas")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # -----------------------------
        # trabajos listos para entregar
        # -----------------------------

        ready_box = QGroupBox("Listos para entregar")
        ready_layout = QVBoxLayout()

        self.ready_table = QTableWidget()
        self.ready_table.setColumnCount(4)
        self.ready_table.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "Equipo",
            "Trabajo"
        ])

        ready_layout.addWidget(self.ready_table)

        btn_layout = QHBoxLayout()

        self.deliver_btn = QPushButton("Marcar como entregado")
        self.deliver_btn.clicked.connect(self.mark_delivered)

        btn_layout.addWidget(self.deliver_btn)

        ready_layout.addLayout(btn_layout)

        ready_box.setLayout(ready_layout)
        layout.addWidget(ready_box)

        # -----------------------------
        # historial
        # -----------------------------

        history_box = QGroupBox("Historial de trabajos entregados")
        history_layout = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "Equipo",
            "Fecha"
        ])

        history_layout.addWidget(self.history_table)

        history_box.setLayout(history_layout)
        layout.addWidget(history_box)

        self.setLayout(layout)

        self.refresh()

    # --------------------------------------------------

    def refresh(self):

        self.load_ready()
        self.load_history()

    # --------------------------------------------------

    def load_ready(self):

        tasks = db.fetchall("""
        SELECT
            tasks.id,
            clients.name as client,
            products.name as product,
            tasks.description
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        LEFT JOIN products ON tasks.product_id = products.id
        WHERE tasks.status='terminado'
        """)

        self.ready_table.setRowCount(len(tasks))

        for row, t in enumerate(tasks):

            self.ready_table.setItem(row, 0, QTableWidgetItem(str(t["id"])))
            self.ready_table.setItem(row, 1, QTableWidgetItem(t["client"] or ""))
            self.ready_table.setItem(row, 2, QTableWidgetItem(t["product"] or ""))
            self.ready_table.setItem(row, 3, QTableWidgetItem(t["description"]))

    # --------------------------------------------------

    def load_history(self):

        tasks = db.fetchall("""
        SELECT
            tasks.id,
            clients.name as client,
            products.name as product,
            tasks.updated_at
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        LEFT JOIN products ON tasks.product_id = products.id
        WHERE tasks.status='entregado'
        ORDER BY tasks.updated_at DESC
        """)

        self.history_table.setRowCount(len(tasks))

        for row, t in enumerate(tasks):

            self.history_table.setItem(row, 0, QTableWidgetItem(str(t["id"])))
            self.history_table.setItem(row, 1, QTableWidgetItem(t["client"] or ""))
            self.history_table.setItem(row, 2, QTableWidgetItem(t["product"] or ""))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(t["updated_at"])))

    # --------------------------------------------------

    def mark_delivered(self):

        row = self.ready_table.currentRow()

        if row < 0:
            return

        id_item = self.ready_table.item(row, 0)

        if id_item is None:
            return

        task_id = int(id_item.text())

        db.execute(
            """
            UPDATE tasks
            SET status='entregado'
            WHERE id=?
            """,
            (task_id,)
        )

        self.refresh()