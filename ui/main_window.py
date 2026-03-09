from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.inventory_view import InventoryView
from ui.jobs_view import JobsView
from ui.clients_view import ClientsView
from ui.purchases_view import PurchasesView
from ui.dashboard_view import DashboardView


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("ERP Taller")

        tabs = QTabWidget()

        tabs.addTab(DashboardView(), "Dashboard")
        tabs.addTab(InventoryView(), "Inventario")
        tabs.addTab(JobsView(), "Trabajos")
        tabs.addTab(ClientsView(), "Clientes")
        tabs.addTab(PurchasesView(), "Compras")

        self.setCentralWidget(tabs)