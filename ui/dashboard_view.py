from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DashboardView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dashboard negocio"))

        self.setLayout(layout)