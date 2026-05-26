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

class DeleteCategory(QWidget):
    def __init__(self, refresh_callback, category_id, category_name):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.category_id = category_id
        self.category_name = category_name
        self.setWindowTitle("Deletar Categoria")
        self.delete_label = QLabel(f"Tem certeza que deseja deletar a categoria {self.category_name}?")
        self.reminder_label = QLabel("A melhor opção é sempre inativá-la pela tela de Atualizar Categoria (Isso evita perda de dados)")
        self.yes_button = QPushButton("Sim")
        self.no_button = QPushButton("Não")
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.delete_label)
        vbox.addWidget(self.reminder_label)
        vbox.addLayout(hbox)
        hbox.addWidget(self.yes_button)
        hbox.addWidget(self.no_button)
        self.delete_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reminder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_label.setObjectName("delete_label")
        self.reminder_label.setObjectName("reminder_label")
        self.yes_button.setObjectName("yes_button")
        self.no_button.setObjectName("no_button")
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
        self.setup_signals()

    def setup_signals(self):
        self.yes_button.clicked.connect(self.delete_category)
        self.no_button.clicked.connect(self.return_window)

    def delete_category(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM categories WHERE category_id = %s", (self.category_id,))
        conn.commit()
        cur.close()
        conn.close()
        self.refresh_callback()
        self.close()

    def return_window(self):
        self.refresh_callback()
        self.close()