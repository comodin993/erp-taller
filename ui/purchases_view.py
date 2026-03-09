from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class PurchasesView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Lista de compras"))

        self.setLayout(layout)