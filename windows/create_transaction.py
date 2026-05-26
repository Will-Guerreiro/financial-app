import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QComboBox, QDateEdit)
from PyQt6.QtCore import Qt
from requests import RequestException
import psycopg
from dotenv import load_dotenv
import os
from connection import get_connection

type_map = {
    "income" : "Ganhos",
    "expense" : "Despesas"
}

class CreateTransaction(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova Transação")
        self.description_label = QLabel("Descrição")
        self.description_input = QLineEdit()
        self.category_name_label = QLabel("Categoria")
        self.category_name_input = QComboBox()
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.amount_label = QLabel("Valor")
        self.amount_input = QLineEdit()
        self.type_label = QLabel("Tipo")
        self.type_input = QComboBox()
        self.date_label = QLabel("Data")
        self.date_input = QDateEdit()
        self.create_transaction_button = QPushButton("Criar")
        self.init_ui()
        self.load_categories()
        self.load_status()
        self.load_types()
        self.setup_signals()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.description_input)
        vbox.addWidget(self.category_name_label)
        vbox.addWidget(self.category_name_input)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.status_input)
        vbox.addWidget(self.amount_label)
        vbox.addWidget(self.amount_input)
        vbox.addWidget(self.type_label)
        vbox.addWidget(self.type_input)
        vbox.addWidget(self.date_label)
        vbox.addWidget(self.date_input)
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        vbox.addWidget(self.create_transaction_button)

        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def load_categories(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT category_id, category_name
            FROM categories
            WHERE is_active = True
        """)
        rows = cur.fetchall()
        conn.close()
        cur.close()
        for row in rows:
            db_value = row[0]
            display_value = row[1]
            self.category_name_input.addItem(display_value, db_value)

    def load_status(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT status
            FROM transactions
        """)
        rows = cur.fetchall()
        conn.close()
        cur.close()
        for row in rows:
            self.status_input.addItem(row[0], row[0])

    def load_types(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT transaction_type
            FROM transactions
        """)
        rows = cur.fetchall()
        conn.close()
        cur.close()
        for row in rows:
            db_value = row[0]
            display_value = type_map.get(db_value, db_value)
            self.type_input.addItem(display_value, db_value)

    def setup_signals(self):
        self.create_transaction_button.clicked.connect(self.create_transaction)

    def create_transaction(self):
        conn = get_connection()
        cur = conn.cursor()
        qdate = self.date_input.date()
        python_date = qdate.toPyDate()
        amount = float(self.amount_input.text())
        cur.execute("""
            INSERT INTO transactions (transaction_description, category_id, status, amount, transaction_type, transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.description_input.text(), self.category_name_input.currentData(), self.status_input.currentData(),
              amount, self.type_input.currentData(), python_date))
        conn.commit()
        cur.close()
        conn.close()
        self.close()