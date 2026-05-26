import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from psycopg import rows
from requests import RequestException
import psycopg
from dotenv import load_dotenv
import os
from connection import get_connection
from windows.create_category import CreateCategory
from windows.delete_category import DeleteCategory
from windows.update_category import UpdateCategory

load_dotenv()
type_map = {
    "income" : "Ganhos",
    "expense" : "Despesas"
}

class CategoriesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Categorias")
        self.create_category_button = QPushButton("Criar Categoria")
        self.edit_category_button = QPushButton("Editar Categoria")
        self.delete_category_button = QPushButton("Deletar Categoria")
        self.init_ui()
        self.load_categories()

    def init_ui(self):
        self.setWindowTitle("Categorias")
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.qtable = QTableWidget()
        vbox.addWidget(self.qtable)
        self.setLayout(vbox)
        vbox.addLayout(hbox)
        hbox.addWidget(self.create_category_button)
        hbox.addWidget(self.edit_category_button)
        hbox.addWidget(self.delete_category_button)
        self.qtable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.qtable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.create_category_button.setObjectName("create_cattegory_button")
        self.edit_category_button.setObjectName("edit_category_button")
        self.delete_category_button.setObjectName("delete_category_button")
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

    def load_categories(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT category_id, category_name, category_description, category_type
                    FROM categories
                    WHERE is_active = true;""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        self.qtable.setRowCount(len(rows))
        self.qtable.setColumnCount(4)
        self.qtable.setHorizontalHeaderLabels([
            "ID", "Nome", "Descrição", "Tipo"
        ])
        for row_index, row_data in enumerate(rows):
            for column_index, value in enumerate(row_data):
                display_value = type_map.get(value, value)
                self.qtable.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(display_value))
                )
                self.qtable.resizeColumnToContents(column_index)
        

    def setup_signals(self):
        self.create_category_button.clicked.connect(self.open_create_category_window)
        self.edit_category_button.clicked.connect(self.open_update_category_window)
        self.delete_category_button.clicked.connect(self.open_delete_category_window)

    def open_create_category_window(self):
        self.create_category_window = CreateCategory(self.load_categories)
        self.create_category_window.show()

    def open_update_category_window(self):
        category_id = self.qtable.item(self.qtable.currentRow(), 0).text()
        category_name = self.qtable.item(self.qtable.currentRow(), 1).text()
        category_description = self.qtable.item(self.qtable.currentRow(), 2).text()
        self.update_category_window = UpdateCategory(self.load_categories, category_id, category_name, category_description)
        self.update_category_window.show()

    def open_delete_category_window(self):
        category_id = self.qtable.item(self.qtable.currentRow(), 0).text()
        category_name = self.qtable.item(self.qtable.currentRow(), 1).text()
        self.delete_category_window = DeleteCategory(self.load_categories, category_id, category_name)
        self.delete_category_window.show()





