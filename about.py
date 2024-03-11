"""
Setting AboutDialog
"""
from PyQt6.QtWidgets import QMessageBox


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        content = """This app records usernames and passwords
_______________________________________
Created by HEV10
"""
        self.setText(content)
