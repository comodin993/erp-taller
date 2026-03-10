from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QLineEdit
)

from tasks.task_manager import TaskManager
from clients.client_manager import ClientManager
from inventory.product_manager import ProductManager


class TasksView(QWidget):

    def __init__(self):
        super().__init__()

        self.tm = TaskManager()
        self.cm = ClientManager()
        self.pm = ProductManager()

        layout = QVBoxLayout()

        # ----------------------
        # formulario
        # ----------------------

        form = QHBoxLayout()

        self.client = QComboBox()
        self.product = QComboBox()

        self.description = QLineEdit()
        self.description.setPlaceholderText("Trabajo")

        add_btn = QPushButton("Crear trabajo")
        add_btn.clicked.connect(self.create_task)

        form.addWidget(self.client)
        form.addWidget(self.product)
        form.addWidget(self.description)
        form.addWidget(add_btn)

        layout.addLayout(form)

        # ----------------------
        # tabla
        # ----------------------

        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Cliente",
            "Producto",
            "Trabajo",
            "Estado",
            "Acción"
        ])

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_selectors()
        self.refresh()

    # ----------------------

    def load_selectors(self):

        self.client.clear()
        self.product.clear()

        clients = self.cm.all()
        products = self.pm.all()

        for c in clients:
            self.client.addItem(c["name"], c["id"])

        for p in products:
            self.product.addItem(p["name"], p["id"])

    # ----------------------

    def create_task(self):

        client_id = self.client.currentData()
        product_id = self.product.currentData()
        description = self.description.text()

        if not description:
            return

        self.tm.create(client_id, product_id, description)

        self.description.clear()

        self.refresh()

    # ----------------------

    def refresh(self):

        tasks = self.tm.all()

        self.table.setRowCount(len(tasks))

        for row, t in enumerate(tasks):

            self.table.setItem(row, 0, QTableWidgetItem(str(t["client"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(t["product"])))
            self.table.setItem(row, 2, QTableWidgetItem(t["description"]))
            self.table.setItem(row, 3, QTableWidgetItem(t["status"]))

            btn = QPushButton("Terminar")

            btn.clicked.connect(
                lambda _, tid=t["id"]: self.finish_task(tid)
            )

            self.table.setCellWidget(row, 4, btn)

    # ----------------------

    def finish_task(self, task_id):

        self.tm.update_status(task_id, "terminado")

        self.refresh()