from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)

import json
import os


class ProductDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nuevo Producto")
        self.resize(400, 300)

        self.catalog = self.load_catalog()

        layout = QVBoxLayout()
        form = QFormLayout()

        # Tipo
        self.type_combo = QComboBox()
        self.type_combo.addItems(self.catalog["types"])
        self.type_combo.currentTextChanged.connect(self.update_brands)

        # Marca
        self.brand_combo = QComboBox()
        self.brand_combo.currentTextChanged.connect(self.update_models)

        # Modelo
        self.model_combo = QComboBox()

        # Condición
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(self.catalog["conditions"])

        # Ubicación
        self.location_combo = QComboBox()
        self.location_combo.addItems(self.catalog["locations"])

        # Precio
        self.price_input = QLineEdit()

        # Stock
        self.stock_input = QLineEdit()

        form.addRow("Tipo", self.type_combo)
        form.addRow("Marca", self.brand_combo)
        form.addRow("Modelo", self.model_combo)
        form.addRow("Condición", self.condition_combo)
        form.addRow("Ubicación", self.location_combo)
        form.addRow("Precio", self.price_input)
        form.addRow("Stock inicial", self.stock_input)

        layout.addLayout(form)

        # Botones
        buttons = QHBoxLayout()

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)

        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.update_brands(self.type_combo.currentText())

    def load_catalog(self):

        path = os.path.join("data", "catalog.json")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_brands(self, type_name):

        self.brand_combo.clear()

        brands = self.catalog["brands"].get(type_name, [])

        self.brand_combo.addItems(brands)

        if brands:
            self.update_models(brands[0])

    def update_models(self, brand):

        self.model_combo.clear()

        models = self.catalog["models"].get(brand, [])

        self.model_combo.addItems(models)

    def save(self):

        if not self.price_input.text().isdigit():
            QMessageBox.warning(self, "Error", "Precio inválido")
            return

        if not self.stock_input.text().isdigit():
            QMessageBox.warning(self, "Error", "Stock inválido")
            return

        self.product_data = {
            "type": self.type_combo.currentText(),
            "brand": self.brand_combo.currentText(),
            "model": self.model_combo.currentText(),
            "condition": self.condition_combo.currentText(),
            "location": self.location_combo.currentText(),
            "price": int(self.price_input.text()),
            "stock": int(self.stock_input.text())
        }

        self.accept()