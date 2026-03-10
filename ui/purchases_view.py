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


class PurchasesView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Compras y reposición")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # --------------------------------
        # Sugerencias de compra
        # --------------------------------

        suggest_box = QGroupBox("Sugerencias de reposición")
        suggest_layout = QVBoxLayout()

        self.suggest_table = QTableWidget()
        self.suggest_table.setColumnCount(4)
        self.suggest_table.setHorizontalHeaderLabels([
            "Producto",
            "Stock actual",
            "Stock mínimo",
            "Comprar"
        ])

        suggest_layout.addWidget(self.suggest_table)

        # botón registrar compra
        btn_layout = QHBoxLayout()

        self.buy_btn = QPushButton("Registrar compra")
        self.buy_btn.clicked.connect(self.register_purchase)

        btn_layout.addWidget(self.buy_btn)

        suggest_layout.addLayout(btn_layout)

        suggest_box.setLayout(suggest_layout)
        layout.addWidget(suggest_box)

        # --------------------------------
        # Historial de compras
        # --------------------------------

        history_box = QGroupBox("Historial de compras")
        history_layout = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "ID",
            "Producto",
            "Cantidad",
            "Fecha"
        ])

        history_layout.addWidget(self.history_table)

        history_box.setLayout(history_layout)
        layout.addWidget(history_box)

        self.setLayout(layout)

        self.refresh()

    # -------------------------------------

    def refresh(self):

        self.load_suggestions()
        self.load_history()

    # -------------------------------------

    def load_suggestions(self):

        products = db.fetchall("""
        SELECT
            id,
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

        suggest = []

        for p in products:

            if p["stock"] < p["stock_min"]:

                buy = p["stock_min"] - p["stock"]

                suggest.append({
                    "id": p["id"],
                    "name": p["name"],
                    "stock": p["stock"],
                    "min": p["stock_min"],
                    "buy": buy
                })

        self.suggest_table.setRowCount(len(suggest))

        for row, p in enumerate(suggest):

            self.suggest_table.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.suggest_table.setItem(row, 1, QTableWidgetItem(str(p["stock"])))
            self.suggest_table.setItem(row, 2, QTableWidgetItem(str(p["min"])))
            self.suggest_table.setItem(row, 3, QTableWidgetItem(str(p["buy"])))

    # -------------------------------------

    def load_history(self):

        purchases = db.fetchall("""
        SELECT
            purchases.id,
            products.name as product,
            purchases.quantity,
            purchases.date
        FROM purchases
        LEFT JOIN products ON purchases.product_id = products.id
        ORDER BY purchases.date DESC
        """)

        self.history_table.setRowCount(len(purchases))

        for row, p in enumerate(purchases):

            self.history_table.setItem(row, 0, QTableWidgetItem(str(p["id"])))
            self.history_table.setItem(row, 1, QTableWidgetItem(p["product"] or ""))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(p["quantity"])))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(p["date"])))

    # -------------------------------------

    def register_purchase(self):

        row = self.suggest_table.currentRow()

        if row < 0:
            return
        
        
        

        name_item = self.suggest_table.item(row, 0)
        qty_item = self.suggest_table.item(row, 3)

        if name_item is None or qty_item is None:
            return

        product_name = name_item.text()
        quantity = int(qty_item.text())

        



        product = db.fetchone(
            "SELECT id FROM products WHERE name=?",
            (product_name,)
        )

        if not product:
            return

        db.execute(
            """
            INSERT INTO purchases (product_id, quantity)
            VALUES (?, ?)
            """,
            (product["id"], quantity)
        )

        self.refresh()