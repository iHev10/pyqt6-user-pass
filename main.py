from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QTextEdit
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
        add_userpass_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_userpass_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Title", "Username", "Password", "Info"))
        # self.table.verticalHeader().setVisible(False)
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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADD new user-pass")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.title = QLineEdit()
        self.title.setPlaceholderText("Title")
        layout.addWidget(self.title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        layout.addWidget(self.password)

        self.extra_info = QTextEdit()
        self.extra_info.setPlaceholderText("Extra Information")
        layout.addWidget(self.extra_info)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_userpass)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_userpass(self):
        title = self.title.text()
        user = self.username.text()
        password = self.password.text()
        extra_info = self.extra_info.toPlainText()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO userpass (Title, Username, Password, Info) VALUES (?, ?, ?, ?)",
                       (title, user, password, extra_info))
        connection.commit()
        cursor.close()
        connection.close()
        user_pass_app.load_data()
        print(title, user, password, extra_info)


app = QApplication(sys.argv)
user_pass_app = MainWindow()
user_pass_app.show()
user_pass_app.load_data()
sys.exit(app.exec())
