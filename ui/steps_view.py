from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel
)

from tasks.task_manager import TaskManager


class StepsView(QWidget):

    def __init__(self, task_id):
        super().__init__()

        self.tm = TaskManager()
        self.task_id = task_id

        layout = QVBoxLayout()

        title = QLabel("Subtareas del trabajo")
        layout.addWidget(title)

        # tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tipo",
            "Descripción",
            "Estado"
        ])

        layout.addWidget(self.table)

        # botón completar
        self.complete_btn = QPushButton("Completar subtarea")
        self.complete_btn.clicked.connect(self.complete_step)

        layout.addWidget(self.complete_btn)

        self.setLayout(layout)

        self.refresh()

    # --------------------------------------

    def refresh(self):

        steps = self.tm.steps(self.task_id)

        self.table.setRowCount(len(steps))

        for row, step in enumerate(steps):

            self.table.setItem(row, 0, QTableWidgetItem(str(step["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(step["type"]))
            self.table.setItem(row, 2, QTableWidgetItem(step["description"]))
            self.table.setItem(row, 3, QTableWidgetItem(step["status"]))

    # --------------------------------------

    def complete_step(self):

        row = self.table.currentRow()

        if row < 0:
            return
        
        item = self.table.item(row, 0)

        if item is None:
            return

        step_id = int(item.text())


        self.tm.complete_step(step_id)

        self.refresh()