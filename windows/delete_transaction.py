import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from requests import RequestException
import psycopg
import os
from connection import get_connection

class DeleteTransaction(QWidget):
    def __init__(self, transaction_id):
        super().__init__()
        self.setWindowTitle("Deletar Categoria")
        self.transaction_id = transaction_id
        self.delete_label = QLabel("Tem certeza que deseja deletar essa transação?")
        self.yes_button = QPushButton("Sim")
        self.no_button = QPushButton("Não")
        self.init_ui()
        self.setup_signals()

    def init_ui(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.delete_label)
        vbox.addLayout(hbox)
        hbox.addWidget(self.yes_button)
        hbox.addWidget(self.no_button)

        self.setStyleSheet("""
                                    QWidget {
                                        background-color: #1e1e2f;
                                        color: #ffffff;
                                        font-family: Arial;
                                        font-size: 14px;
                                    }

                                    QLabel {
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

        self.delete_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setup_signals(self):
        self.yes_button.clicked.connect(self.delete_transaction)
        self.no_button.clicked.connect(self.close_window)

    def delete_transaction(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM transactions
            WHERE transaction_id = %s
        """, (self.transaction_id,))
        conn.commit()
        cur.close()
        conn.close()
        self.close()

    def close_window(self):
        self.close()
