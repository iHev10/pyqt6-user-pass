from database.database import DatabaseConnection
from about import AboutDialog

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QTableWidget,
    QToolBar,
    QStatusBar,
    QTableWidgetItem,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QGridLayout,
    QLabel,
)

import qdarktheme

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User - Pass App")
        self.setMinimumSize(625, 500)

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_userpass_action = QAction(
            QIcon("icons/add.png"), "Add a new user-pass", self)
        add_userpass_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_userpass_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(3, 180)
        self.table.setHorizontalHeaderLabels(
            ("Title", "Username", "Password", "Info"))
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
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM userpass")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
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

    def about(self):
        dialog = AboutDialog()
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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO userpass (Title, Username, Password, Info) VALUES (?, ?, ?, ?)",
                       (title.title(), user, password, extra_info))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()
        print(title, user, password, extra_info)

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was added successfully!")
        confirmation_widget.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search items")

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
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            result = cursor.execute(
                "SELECT * FROM userpass WHERE Title LIKE ?", ("%" + title.title() + "%",))

            txt = ""
            for row in list(result):
                txt += f"\nusername: {row[1]}\npassword: {row[2]}\n"
                txt += "--------------------"
            self.error_message.setText(txt)
            items = main_window.table.findItems(
                title, Qt.MatchFlag.MatchFixedString)
            for item in items:
                print(item.text())
                main_window.table.item(item.row(), 1).setSelected(True)
            cursor.close()
            connection.close()
        except:
            self.error_message.setText(f"'{title}' item does not exist!")


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update user-pass")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()

        title = main_window.table.item(index, 0)
        self.title = QLineEdit(title.text())
        self.title.setPlaceholderText("Title")
        layout.addWidget(self.title)

        username = main_window.table.item(index, 1)
        self.username = QLineEdit(username.text())
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        password = main_window.table.item(index, 2)
        self.password = QLineEdit(password.text())
        self.password.setPlaceholderText("Password")
        layout.addWidget(self.password)

        extra_info = main_window.table.item(index, 3)
        self.extra_info = QTextEdit(extra_info.text())
        self.extra_info.setPlaceholderText("Extra Information")
        layout.addWidget(self.extra_info)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_userpass)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def update_userpass(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE userpass SET Username = ?, Password = ?, Info = ? WHERE Title = ?",
                       (
                           self.username.text(),
                           self.password.text(),
                           self.extra_info.toPlainText(),
                           self.title.text()))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete user-pass")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete?")
        layout.addWidget(confirmation, 0, 0, 1, 2)
        yes_button = QPushButton("Yes")
        layout.addWidget(yes_button, 1, 0)
        no_button = QPushButton("No")
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_userpass)
        no_button.clicked.connect(self.close)

    def delete_userpass(self):
        index = main_window.table.currentRow()
        title = main_window.table.item(index, 0)

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM userpass WHERE Title = ?", (title.text(),))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light", custom_colors={"primary": "#2052a8"})
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()
    sys.exit(app.exec())
