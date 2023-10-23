from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User - Pass App")
        self.setMinimumSize(500, 400)

        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")

        add_userpass_action = QAction("Add a new user-pass", self)
        file_menu_item.addAction(add_userpass_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("#", "Title", "Username", "Password", "Extra info"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM userpass")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
user_pass_app = MainWindow()
user_pass_app.show()
user_pass_app.load_data()
sys.exit(app.exec())
