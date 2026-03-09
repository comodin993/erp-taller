from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ClientsView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Clientes"))

        self.setLayout(layout)