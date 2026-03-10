from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QLabel,
    QComboBox
)

from clients.client_manager import ClientManager


class ClientsView(QWidget):

    def __init__(self):
        super().__init__()

        self.cm = ClientManager()

        layout = QVBoxLayout()

        # -------------------------
        # formulario nuevo cliente
        # -------------------------

        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Teléfono")

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notas")

        add_btn = QPushButton("Agregar")
        add_btn.clicked.connect(self.add_client)

        form.addWidget(self.name_input)
        form.addWidget(self.phone_input)
        form.addWidget(self.notes_input)
        form.addWidget(add_btn)

        layout.addLayout(form)

        # -------------------------
        # tabla clientes
        # -------------------------

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Nombre",
            "Teléfono",
            "Notas",
            "Reputación"
        ])

        layout.addWidget(self.table)

        # -------------------------
        # botones
        # -------------------------

        buttons = QHBoxLayout()

        delete_btn = QPushButton("Eliminar cliente")
        delete_btn.clicked.connect(self.delete_client)

        buttons.addWidget(delete_btn)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.refresh()

    # ----------------------------------

    def reputation_icon(self, value):

        if value == 2:
            return "🟢 Excelente"

        if value == 0:
            return "🔴 Problemático"

        return "🟡 Normal"

    # ----------------------------------

    def refresh(self):

        clients = self.cm.all()

        self.table.setRowCount(len(clients))

        for row, client in enumerate(clients):

            self.table.setItem(row, 0, QTableWidgetItem(client["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(client["phone"] or ""))
            self.table.setItem(row, 2, QTableWidgetItem(client["notes"] or ""))
            self.table.setItem(
                row,
                3,
                QTableWidgetItem(self.reputation_icon(client["reputation"]))
            )

    # ----------------------------------

    def add_client(self):

        name = self.name_input.text().strip()

        if not name:
            return

        phone = self.phone_input.text().strip()
        notes = self.notes_input.text().strip()

        self.cm.create(name, phone, notes)

        self.name_input.clear()
        self.phone_input.clear()
        self.notes_input.clear()

        self.refresh()

    # ----------------------------------

    def delete_client(self):

        row = self.table.currentRow()

        if row < 0:
            return

        client = self.cm.all()[row]

        self.cm.delete(client["id"])

        self.refresh()