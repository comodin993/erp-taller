from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem
)

from inventory.product_manager import ProductManager
from core.search_index import search


class InventoryView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.search = QLineEdit()

        self.search.setPlaceholderText("Buscar...")

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Nombre",
            "Marca",
            "Modelo"
        ])

        layout.addWidget(self.search)

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.pm = ProductManager()

        self.load()

        self.search.textChanged.connect(self.on_search)

    def load(self):

        products = self.pm.all()

        self.populate(products)

    def populate(self, products):

        self.table.setRowCount(len(products))

        for r, p in enumerate(products):

            self.table.setItem(
                r, 0,
                QTableWidgetItem(p["name"])
            )

            self.table.setItem(
                r, 1,
                QTableWidgetItem(p["brand"])
            )

            self.table.setItem(
                r, 2,
                QTableWidgetItem(p["model"])
            )

    def on_search(self):

        products = self.pm.all()

        q = self.search.text()

        results = search(products, q)

        self.populate(results)