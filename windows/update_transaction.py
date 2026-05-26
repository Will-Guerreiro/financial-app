import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QComboBox, QDateEdit)
from PyQt6.QtCore import Qt
from requests import RequestException
import psycopg
import os
from connection import get_connection
from datetime import datetime

type_map = {
    "income" : "Ganhos",
    "expense" : "Despesas",
    True : "Ativa",
    False : "Inativa"
}

class UpdateTransaction(QWidget):
    def __init__(self, refresh_callback, transaction_id, transaction_description, transaction_amount, transaction_date):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Editar Transação")
        self.transaction_id = transaction_id
        self.transaction_description = transaction_description
        self.transaction_amount = transaction_amount
        self.transaction_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
        self.transaction_description_label = QLabel("Descrição")
        self.transaction_description_input = QLineEdit(transaction_description)
        self.transaction_category_label = QLabel("Categoria")
        self.transaction_category_input = QComboBox()
        self.transaction_type_label = QLabel("Tipo")
        self.transaction_type_input = QComboBox()
        self.transaction_status_label = QLabel("Status")
        self.transaction_status_input = QComboBox()
        self.transaction_amount_label = QLabel("Valor")
        self.transaction_amount_input = QLineEdit(transaction_amount)
        self.transaction_date_label = QLabel("Data")
        self.transaction_date_input = QDateEdit()
        self.update_transaction_button = QPushButton("Salvar")
        self.init_ui()
        self.load_categories()
        self.load_types()
        self.load_status()
        self.setup_signals()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.transaction_description_label)
        vbox.addWidget(self.transaction_description_input)
        vbox.addWidget(self.transaction_category_label)
        vbox.addWidget(self.transaction_category_input)
        vbox.addWidget(self.transaction_type_label)
        vbox.addWidget(self.transaction_type_input)
        vbox.addWidget(self.transaction_status_label)
        vbox.addWidget(self.transaction_status_input)
        vbox.addWidget(self.transaction_amount_label)
        vbox.addWidget(self.transaction_amount_input)
        vbox.addWidget(self.transaction_date_label)
        vbox.addWidget(self.transaction_date_input)
        self.transaction_date_input.setDisplayFormat("dd-MM-yyyy")
        self.transaction_date_input.setDate(self.transaction_date)
        vbox.addWidget(self.update_transaction_button)

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
            SELECT DISTINCT category_id, category_name
            FROM categories
            WHERE is_active = True
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            self.transaction_category_input.addItem(row[1], row[0])

    def load_types(self):
         conn = get_connection()
         cur = conn.cursor()
         cur.execute("""
            SELECT DISTINCT transaction_type
            FROM transactions
         """)
         rows = cur.fetchall()
         cur.close()
         conn.close()
         for row in rows:
             db_value = row[0]
             display_value = type_map.get(db_value, db_value)
             self.transaction_type_input.addItem(display_value, db_value)

    def load_status(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT status
            FROM transactions
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            self.transaction_status_input.addItem(row[0], row[0])

    def setup_signals(self):
        self.update_transaction_button.clicked.connect(self.update_transaction)

    def update_transaction(self):
        conn = get_connection()
        cur = conn.cursor()
        amount = float(self.transaction_amount_input.text())
        qdate = self.transaction_date_input.date()
        python_date = qdate.toPyDate()
        cur.execute("""
            UPDATE transactions
            SET transaction_description = %s,
            category_id = %s,
            transaction_type = %s,
            status = %s,
            amount = %s,
            transaction_date = %s
            WHERE transaction_id = %s
        """, (self.transaction_description_input.text(), self.transaction_category_input.currentData(),
              self.transaction_type_input.currentData(), self.transaction_status_input.currentData(),
              amount, python_date, self.transaction_id))
        conn.commit()
        cur.close()
        conn.close()
        self.refresh_callback()
        self.close()