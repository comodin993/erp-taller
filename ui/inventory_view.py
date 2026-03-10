from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog
)

from inventory.product_manager import ProductManager
from inventory.piece_manager import PieceManager
from purchases.purchase_manager import PurchaseManager
from core.search_index import search
from ui.product_dialog import ProductDialog


class InventoryView(QWidget):

    def __init__(self):
        super().__init__()

        self.pm = ProductManager()
        self.pcm = PieceManager()
        self.purch = PurchaseManager()

        layout = QVBoxLayout()

        # buscador
        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.search)

        # botones
        buttons = QHBoxLayout()

        self.btn_add_product = QPushButton("Nuevo producto")
        buttons.addWidget(self.btn_add_product)

        layout.addLayout(buttons)

        # tabla
        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "Nombre",
            "Marca",
            "Modelo",
            "Stock",
            "Stock mínimo",
            "Precio",
            "Compras"
        ])

        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # conexiones
        self.search.textChanged.connect(self.on_search)
        self.btn_add_product.clicked.connect(self.add_product_dialog)

        # cargar
        self.load()

    # --------------------------

    def add_product_dialog(self):

        dialog = ProductDialog(self)

        if dialog.exec():

            data = dialog.product_data

            brand = data.get("brand", "")
            model = data.get("model", "")

            name = f"{brand} {model}"

            self.pm.create(name, brand, model)

            self.load()

    # --------------------------

    def load(self):

        products = self.pm.all()
        self.populate(products)

    # --------------------------

    def populate(self, products):

        self.table.setRowCount(len(products))

        for r, p in enumerate(products):

            stock = self.pcm.count_by_product(p["id"])

            self.table.setItem(r, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(r, 1, QTableWidgetItem(p["brand"]))
            self.table.setItem(r, 2, QTableWidgetItem(p["model"]))
            self.table.setItem(r, 3, QTableWidgetItem(str(stock)))

            if "stock_min" in p:
                self.table.setItem(r, 4, QTableWidgetItem(str(p["stock_min"])))
            else:
                self.table.setItem(r, 4, QTableWidgetItem("-"))

            if "price" in p:
                self.table.setItem(r, 5, QTableWidgetItem(str(p["price"])))
            else:
                self.table.setItem(r, 5, QTableWidgetItem("-"))

            btn = QPushButton("+1")

            btn.clicked.connect(
                lambda _, pid=p["id"]: self.add_purchase(pid)
            )

            self.table.setCellWidget(r, 6, btn)

    # --------------------------

    def add_purchase(self, product_id):

        self.purch.add(product_id, 1)
        self.load()

    # --------------------------

    def on_search(self):

        products = self.pm.all()
        q = self.search.text()

        results = search(products, q)

        self.populate(results)