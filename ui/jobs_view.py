from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class JobsView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Trabajos"))

        self.setLayout(layout)