from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,           
    QGridLayout,
    QPushButton, QLineEdit, QLabel
)
from MainWindow import MainWindow
from Login import Login
import sys

def main():
    app = QApplication() 
    login = Login()
    with open('stylesheet.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)     
    login.show()
    sys.exit(app.exec())

main()