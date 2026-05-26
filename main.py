import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt6.QtCore import Qt
from requests import RequestException
from windows.categories_window import CategoriesWindow
from windows.transactions_window import TransactionsWindow

class FinancialApp(QWidget):

    def __init__(self):
        super().__init__()
        self.welcome_label = QLabel("Organização Financeira", self)
        self.see_categories_button = QPushButton("Ver Categorias", self)
        self.see_transactions_button = QPushButton("Ver Transações", self)
        self.categories_window = None
        self.transactions_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Organização Financeira")
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.welcome_label)

        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(vbox)
        vbox.addLayout(hbox)

        hbox.addWidget(self.see_categories_button)
        hbox.addWidget(self.see_transactions_button)

        self.welcome_label.setObjectName("welcome_label")
        self.see_categories_button.setObjectName("see_categories_button")
        self.see_transactions_button.setObjectName("see_transactions_button")
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Arial;
                font-size: 14px;
            }

            QLabel#welcome_label {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 15px;
            }

            QPushButton {
                background-color: #303aab;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #1b5fa7;
            }

            QPushButton:pressed {
                background-color: #144a82;
            }
        """)
        self.setup_signals()

    def setup_signals(self):
        self.see_categories_button.clicked.connect(self.open_categories_window)
        self.see_transactions_button.clicked.connect(self.open_transactions_window)

    def open_categories_window(self):
        self.categories_window = CategoriesWindow()
        self.categories_window.show()

    def open_transactions_window(self):
        self.transactions_window = TransactionsWindow()
        self.transactions_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    financial_app = FinancialApp()
    financial_app.show()
    sys.exit(app.exec())