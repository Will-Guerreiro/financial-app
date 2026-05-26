import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from requests import RequestException
import psycopg
from dotenv import load_dotenv
import os
from connection import get_connection


load_dotenv()
type_map = {
    "income" : "Ganhos",
    "expense" : "Despesas"
}

class CreateCategory(QWidget):
    def __init__(self, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Criar Categoria")
        self.name_label = QLabel("Nome da Categoria")
        self.name_input = QLineEdit()
        self.description_label = QLabel("Descrição da Categoria")
        self.description_input = QLineEdit()
        self.type_label = QLabel("Tipo da Categoria")
        self.type_input = QComboBox()
        self.create_button = QPushButton("Criar")
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        self.setLayout(vbox)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        hbox.addWidget(self.name_label)
        hbox.addWidget(self.name_input)
        hbox2.addWidget(self.description_label)
        hbox2.addWidget(self.description_input)
        hbox3.addWidget(self.type_label)
        hbox3.addWidget(self.type_input)
        vbox.addWidget(self.create_button)

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_label.setObjectName("name_label")
        self.name_input.setObjectName("name_input")
        self.description_label.setObjectName("description_label")
        self.description_input.setObjectName("description_input")
        self.type_label.setObjectName("type_label")
        self.type_input.setObjectName("type_input")
        self.create_button.setObjectName("create_button")
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

        self.load_types()
        self.setup_signals()

    def setup_signals(self):
        self.create_button.clicked.connect(self.create_category)

    def create_category(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO categories (category_name, category_description, category_type)
                    values (%s, %s, %s);
                """, (self.name_input.text(), self.description_input.text(), self.type_input.currentData()))
        conn.commit()
        cur.close()
        conn.close()
        self.refresh_callback()
        self.close()

    def load_types(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT category_type from categories;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            db_value = row[0]
            display_value = type_map.get(db_value, db_value)
            self.type_input.addItem(display_value, db_value)
