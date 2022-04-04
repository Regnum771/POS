from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,           
    QGridLayout,
    QPushButton, QLineEdit, QLabel
)
from MainWindow import MainWindow
from Model import Model
import sys

class Login(QMainWindow):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)
        self.title = "Login"
        self.init_gui()
    
    def init_gui(self):
        #Layout Management
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QGridLayout(self.window)
        self.window.setLayout(self.layout)

        self.username_textbox = QLineEdit("username", self)
        self.username_label = QLabel("Username", self)

        self.password_textbox = QLineEdit("username", self)
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.password_label = QLabel("Password", self)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.forgot_button = QPushButton("Forgot Password", self)

        self.layout.addWidget(self.username_label, 0, 0)
        self.layout.addWidget(self.username_textbox, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.password_textbox, 1, 1)
        self.layout.addWidget(self.login_button, 2, 0)
        self.layout.addWidget(self.forgot_button, 2, 1)

    def login(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()

        try:
            self.model = Model(username, password)
        except:
            print("Connection Failed")
            return
        
        self.main_window = MainWindow(self.model)
        self.main_window.show()
        self.hide()

    def closeEvent(self, event):
        return 0