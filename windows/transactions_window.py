import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QComboBox, QDateEdit, QCheckBox)
from PyQt6.QtCore import Qt
import os
from connection import get_connection
from windows.create_transaction import CreateTransaction
from windows.update_transaction import UpdateTransaction
from windows.delete_transaction import DeleteTransaction

type_map = {
    "income" : "Ganhos",
    "expense" : "Despesas"
}

class TransactionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transações")
        self.search_transaction_button = QPushButton("Buscar Transações")
        self.filters_label = QLabel("Filtros")
        self.description_label = QLabel("Descrição")
        self.description_input = QLineEdit()
        self.category_label = QLabel("Categoria")
        self.category_input = QComboBox()
        self.type_label = QLabel("Tipo")
        self.type_input = QComboBox()
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.activate_date_filter = QCheckBox("Ativar filtro de data")
        self.date_from_label = QLabel("Data Inicial")
        self.date_from_input = QDateEdit()
        self.date_to_label = QLabel("Data Final")
        self.date_to_input = QDateEdit()
        self.min_amount_label = QLabel("Valor Mínimo")
        self.min_amount_input = QLineEdit()
        self.max_amount_label = QLabel("Valor Máximo")
        self.max_amount_input = QLineEdit()
        self.show_filters_button = QPushButton("Mostrar Filtros")
        self.hide_filters_button = QPushButton("Esconder Filtros")
        self.create_transaction_button = QPushButton("Nova Transação")
        self.update_transaction_button = QPushButton("Editar Transação")
        self.delete_transaction_button = QPushButton("Deletar Transação")
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        vbox_date = QVBoxLayout()
        vbox_date2 = QVBoxLayout()
        vbox_amount = QVBoxLayout()
        vbox_amount2 = QVBoxLayout()
        hbox_date = QHBoxLayout()
        hbox_amount = QHBoxLayout()
        hbox_crud = QHBoxLayout()
        self.qtable = QTableWidget()
        self.setLayout(vbox)
        vbox.addWidget(self.filters_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.description_input)
        vbox.addWidget(self.category_label)
        vbox.addWidget(self.category_input)
        vbox.addWidget(self.type_label)
        vbox.addWidget(self.type_input)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.status_input)
        vbox.addLayout(hbox_date)
        hbox_date.addLayout(vbox_date)
        hbox_date.addLayout(vbox_date2)
        vbox_date.addWidget(self.date_from_label)
        vbox_date.addWidget(self.date_from_input)
        self.date_from_input.setDisplayFormat("dd-MM-yyyy")
        vbox_date2.addWidget(self.date_to_label)
        vbox_date2.addWidget(self.date_to_input)
        self.date_to_input.setDisplayFormat("dd-MM-yyyy")
        vbox.addWidget(self.activate_date_filter)
        vbox.addLayout(hbox_amount)
        hbox_amount.addLayout(vbox_amount)
        hbox_amount.addLayout(vbox_amount2)
        vbox_amount.addWidget(self.min_amount_label)
        vbox_amount.addWidget(self.min_amount_input)
        vbox_amount2.addWidget(self.max_amount_label)
        vbox_amount2.addWidget(self.max_amount_input)
        vbox.addWidget(self.search_transaction_button)
        vbox.addWidget(self.show_filters_button)
        vbox.addWidget(self.hide_filters_button)
        vbox.addWidget(self.qtable)
        self.qtable.hide()
        vbox.addLayout(hbox_crud)
        hbox_crud.addWidget(self.create_transaction_button)
        hbox_crud.addWidget(self.update_transaction_button)
        hbox_crud.addWidget(self.delete_transaction_button)
        self.create_transaction_button.hide()
        self.update_transaction_button.hide()
        self.delete_transaction_button.hide()

        self.filters_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search_transaction_button.setObjectName("search_transaction_button")
        self.filters_label.setObjectName("filters_label")
        self.description_label.setObjectName("description_label")
        self.description_input.setObjectName("description_input")
        self.category_label.setObjectName("category_label")
        self.category_input.setObjectName("category_input")
        self.type_label.setObjectName("type_label")
        self.type_input.setObjectName("type_input")
        self.date_to_label.setObjectName("date_to_label")
        self.date_to_input.setObjectName("date_to_input")
        self.date_from_label.setObjectName("date_from_label")
        self.date_from_input.setObjectName("date_from_input")
        self.min_amount_label.setObjectName("min_amount_label")
        self.min_amount_input.setObjectName("min_amount_input")
        self.max_amount_label.setObjectName("max_amount_label")
        self.max_amount_input.setObjectName("max_amount_input")
        self.show_filters_button.setObjectName("show_filters_button")
        self.hide_filters_button.setObjectName("hide_filters_button")

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
        self.category_input.addItem("Todas", None)
        self.type_input.addItem("Todos", None)
        self.status_input.addItem("Todos", None)
        self.load_categories()
        self.load_types()
        self.load_status()

    def setup_signals(self):
        self.search_transaction_button.clicked.connect(self.search_transactions)
        self.show_filters_button.clicked.connect(self.show_filters)
        self.hide_filters_button.clicked.connect(self.hide_filters)
        self.create_transaction_button.clicked.connect(self.create_transaction_window)
        self.update_transaction_button.clicked.connect(self.update_transaction_window)
        self.delete_transaction_button.clicked.connect(self.delete_transaction_window)

    def search_transactions(self):
        conn = get_connection()
        cur = conn.cursor()
        query = """SELECT t.transaction_id, t.transaction_description, c.category_name, t.transaction_type, t.status, t.amount, t.transaction_date
                       FROM transactions t
                       JOIN categories c
                       ON t.category_id = c.category_id
                       WHERE 1 = 1"""
        params = []
        description_text = self.description_input.text().strip()
        if description_text:
            query += " AND t.transaction_description ILIKE %s"
            params.append(f"%{description_text}%")
        category_id = self.category_input.currentData()
        if category_id:
            query += " AND t.category_id = %s"
            params.append(category_id)
        category_type = self.type_input.currentData()
        if category_type:
            query += " AND t.transaction_type = %s"
            params.append(category_type)
        status = self.status_input.currentData()
        if status:
            query += " AND t.status = %s"
            params.append(status)
        qdate = self.date_from_input.date()
        python_date = qdate.toPyDate()
        if self.activate_date_filter.isChecked():
            query+= " AND t.transaction_date >= %s"
            params.append(python_date)
        qdate2 = self.date_to_input.date()
        python_date2 = qdate2.toPyDate()
        if self.activate_date_filter.isChecked():
            query += " AND t.transaction_date <= %s"
            params.append(python_date2)
        min_amount_text = self.min_amount_input.text().strip()
        if min_amount_text:
            min_amount = float(min_amount_text)
            query += " AND t.amount >= %s"
            params.append(min_amount)
        max_amount_text = self.max_amount_input.text().strip()
        if max_amount_text:
            max_amount = float(max_amount_text)
            query += " AND t.amount <= %s"
            params.append(max_amount)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        self.qtable.setRowCount(len(rows))
        self.qtable.setColumnCount(7)
        self.qtable.setHorizontalHeaderLabels([
            "ID", "Descrição", "Categoria", "Tipo", "Status", "Valor", "Data"
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
        self.showMaximized()
        self.hide_filters()
        self.qtable.show()
        self.create_transaction_button.show()
        self.update_transaction_button.show()
        self.delete_transaction_button.show()

    def hide_filters(self):
        self.search_transaction_button.hide()
        self.filters_label.hide()
        self.description_label.hide()
        self.description_input.hide()
        self.category_label.hide()
        self.category_input.hide()
        self.type_label.hide()
        self.type_input.hide()
        self.status_label.hide()
        self.status_input.hide()
        self.date_to_label.hide()
        self.date_to_input.hide()
        self.date_from_label.hide()
        self.date_from_input.hide()
        self.min_amount_label.hide()
        self.min_amount_input.hide()
        self.max_amount_label.hide()
        self.max_amount_input.hide()
        self.activate_date_filter.hide()

    def show_filters(self):
        self.search_transaction_button.show()
        self.filters_label.show()
        self.description_label.show()
        self.description_input.show()
        self.category_label.show()
        self.category_input.show()
        self.type_label.show()
        self.type_input.show()
        self.status_label.show()
        self.status_input.show()
        self.date_to_label.show()
        self.date_to_input.show()
        self.date_from_label.show()
        self.date_from_input.show()
        self.min_amount_label.show()
        self.min_amount_input.show()
        self.max_amount_label.show()
        self.max_amount_input.show()
        self.activate_date_filter.show()

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
            db_value = row[0]
            display_value = row[1]
            self.category_input.addItem(display_value, db_value)

    def load_types(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT category_type
            FROM categories;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            db_value = row[0]
            display_value = type_map.get(db_value, db_value)
            self.type_input.addItem(display_value, db_value)

    def create_transaction_window(self):
        self.create_transaction_window = CreateTransaction()
        self.create_transaction_window.show()

    def update_transaction_window(self):
        transaction_id = self.qtable.item(self.qtable.currentRow(), 0).text()
        transaction_description = self.qtable.item(self.qtable.currentRow(), 1).text()
        transaction_amount = self.qtable.item(self.qtable.currentRow(), 5).text()
        transaction_date = self.qtable.item(self.qtable.currentRow(), 6).text()
        self.update_transaction_window = UpdateTransaction(self.search_transactions, transaction_id, transaction_description, transaction_amount, transaction_date)
        self.update_transaction_window.show()

    def load_status(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT status
            FROM transactions;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            self.status_input.addItem(row[0], row[0])

    def delete_transaction_window(self):
        transaction_id = self.qtable.item(self.qtable.currentRow(), 0).text()
        self.delete_transaction_window = DeleteTransaction(transaction_id)
        self.delete_transaction_window.show()