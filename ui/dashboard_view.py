from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox
)

from tasks.task_manager import TaskManager
from core.database import db


class DashboardView(QWidget):

    def __init__(self):
        super().__init__()

        self.tm = TaskManager()

        layout = QVBoxLayout()

        title = QLabel("Dashboard del Taller")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # -----------------------------
        # Checklist de subtareas
        # -----------------------------

        checklist_box = QGroupBox("Checklist de tareas pendientes")
        checklist_layout = QVBoxLayout()

        self.steps_table = QTableWidget()
        self.steps_table.setColumnCount(4)
        self.steps_table.setHorizontalHeaderLabels([
            "Trabajo",
            "Tipo",
            "Descripción",
            "Estado"
        ])

        checklist_layout.addWidget(self.steps_table)
        checklist_box.setLayout(checklist_layout)

        layout.addWidget(checklist_box)

        # -----------------------------
        # Trabajos activos
        # -----------------------------

        tasks_box = QGroupBox("Trabajos activos")
        tasks_layout = QVBoxLayout()

        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(3)
        self.tasks_table.setHorizontalHeaderLabels([
            "Cliente",
            "Equipo",
            "Estado"
        ])

        tasks_layout.addWidget(self.tasks_table)
        tasks_box.setLayout(tasks_layout)

        layout.addWidget(tasks_box)

        # -----------------------------
        # Productos bajo stock
        # -----------------------------

        stock_box = QGroupBox("Productos con bajo stock")
        stock_layout = QVBoxLayout()

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels([
            "Producto",
            "Stock",
            "Stock mínimo"
        ])

        stock_layout.addWidget(self.stock_table)
        stock_box.setLayout(stock_layout)

        layout.addWidget(stock_box)

        self.setLayout(layout)

        self.refresh()

    # -------------------------------------------------

    def refresh(self):

        self.load_steps()
        self.load_tasks()
        self.load_low_stock()

    # -------------------------------------------------

    def load_steps(self):

        steps = db.fetchall("""
        SELECT
            tasks.description as task,
            task_steps.type,
            task_steps.description,
            task_steps.status
        FROM task_steps
        LEFT JOIN tasks ON task_steps.task_id = tasks.id
        WHERE task_steps.status='pending'
        """)

        self.steps_table.setRowCount(len(steps))

        for row, step in enumerate(steps):

            self.steps_table.setItem(row, 0, QTableWidgetItem(step["task"]))
            self.steps_table.setItem(row, 1, QTableWidgetItem(step["type"]))
            self.steps_table.setItem(row, 2, QTableWidgetItem(step["description"]))
            self.steps_table.setItem(row, 3, QTableWidgetItem(step["status"]))

    # -------------------------------------------------

    def load_tasks(self):

        tasks = db.fetchall("""
        SELECT
            clients.name as client,
            products.name as product,
            tasks.status
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        LEFT JOIN products ON tasks.product_id = products.id
        WHERE tasks.status != 'terminado'
        """)

        self.tasks_table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):

            self.tasks_table.setItem(row, 0, QTableWidgetItem(task["client"] or ""))
            self.tasks_table.setItem(row, 1, QTableWidgetItem(task["product"] or ""))
            self.tasks_table.setItem(row, 2, QTableWidgetItem(task["status"]))

    # -------------------------------------------------

    def load_low_stock(self):

        products = db.fetchall("""
        SELECT
            name,
            stock_min,
            (
                SELECT COUNT(*)
                FROM pieces
                WHERE pieces.product_id = products.id
                AND status='stock'
            ) as stock
        FROM products
        """)

        low = []

        for p in products:
            if p["stock"] <= p["stock_min"]:
                low.append(p)

        self.stock_table.setRowCount(len(low))

        for row, p in enumerate(low):

            self.stock_table.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.stock_table.setItem(row, 1, QTableWidgetItem(str(p["stock"])))
            self.stock_table.setItem(row, 2, QTableWidgetItem(str(p["stock_min"])))