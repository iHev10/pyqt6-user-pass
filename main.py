from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QTextEdit, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User - Pass App")
        self.setMinimumSize(500, 400)

        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")
        edit_menu_item = self.menuBar().addMenu("&edit")

        add_userpass_action = QAction(QIcon("icons/add.png"), "Add a new user-pass", self)
        add_userpass_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_userpass_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Title", "Username", "Password", "Info"))
        # self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_userpass_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_click)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def cell_click(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        edit = EditDialog()
        edit.exec()

    def delete(self):
        delete = DeleteDialog()
        delete.exec()


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
                       (title.title(), user, password, extra_info))
        connection.commit()
        cursor.close()
        connection.close()
        user_pass_app.load_data()
        print(title, user, password, extra_info)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search items")
        self.setFixedWidth(210)
        self.setFixedHeight(110)

        layout = QVBoxLayout()

        self.title = QLineEdit()
        self.title.setPlaceholderText("Title")
        layout.addWidget(self.title)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.error_message = QLabel("")
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def search(self):
        try:
            title = self.title.text()
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM userpass WHERE Title = ?", (title.title(),))
            row = list(result)[0]
            self.error_message.setText(f"username: {row[1]}\npassword: {row[2]}")
            items = user_pass_app.table.findItems(title, Qt.MatchFlag.MatchFixedString)
            for item in items:
                print(item.text())
                user_pass_app.table.item(item.row(), 1).setSelected(True)
            cursor.close()
            connection.close()
        except:
            self.error_message.setText(f"'{title}' item does not exist!")


class EditDialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
user_pass_app = MainWindow()
user_pass_app.show()
user_pass_app.load_data()
sys.exit(app.exec())
