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
    "expense" : "Despesas",
    True : "Ativa",
    False : "Inativa"
}

class UpdateCategory(QWidget):
    def __init__(self,refresh_callback, category_id, category_name, category_description):
        super().__init__()
        self.setWindowTitle("Atualizar Categoria")
        self.refresh_callback = refresh_callback
        self.category_id = category_id
        self.name_label = QLabel("Nome da Categoria")
        self.name_input = QLineEdit(category_name)
        self.description_label = QLabel("Descrição da Categoria")
        self.description_input = QLineEdit(category_description)
        self.type_label = QLabel("Tipo da Categoria")
        self.type_input = QComboBox()
        self.active_label = QLabel("Ativo")
        self.active_input = QComboBox()
        self.update_button = QPushButton("Atualizar")
        self.init_ui()
        self.load_types_active()

    def init_ui(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        self.setLayout(vbox)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        hbox.addWidget(self.name_label)
        hbox.addWidget(self.name_input)
        hbox2.addWidget(self.description_label)
        hbox2.addWidget(self.description_input)
        hbox3.addWidget(self.type_label)
        hbox3.addWidget(self.type_input)
        hbox4.addWidget(self.active_label)
        hbox4.addWidget(self.active_input)
        vbox.addWidget(self.update_button)

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.active_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def load_types_active(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT category_type from categories;
        """)
        rows = cur.fetchall()
        for row in rows:
            db_value = row[0]
            display_value = type_map.get(db_value, db_value)
            self.type_input.addItem(display_value, db_value)
        cur.execute("""
            SELECT DISTINCT is_active from categories;
        """)
        rows = cur.fetchall()
        for row in rows:
            db_value = row[0]
            display_value = type_map.get(db_value, db_value)
            self.active_input.addItem(display_value, db_value)

    def setup_signals(self):
        self.update_button.clicked.connect(self.update_category)

    def update_category(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE categories
            SET category_name = %s,
            category_description = %s,
            category_type = %s,
            is_active = %s
            where category_id = %s
        """, (self.name_input.text(), self.description_input.text(), self.type_input.currentData(), self.active_input.currentData(), self.category_id))
        conn.commit()
        cur.close()
        conn.close()
        self.refresh_callback()
        self.close()
