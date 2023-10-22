from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout,\
    QLabel, QLineEdit, QPushButton, QTableWidget
from PyQt6.QtGui import QAction
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User - Pass App")

        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")

        add_userpass_action = QAction("Add a new user-pass", self)
        file_menu_item.addAction(add_userpass_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("#", "Title", "Username", "Password", "Extra info"))
        self.setCentralWidget(self.table)





app = QApplication(sys.argv)
user_pass_app = MainWindow()
user_pass_app.show()
sys.exit(app.exec())