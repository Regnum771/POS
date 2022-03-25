from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,           
    QVBoxLayout, 
    QPushButton,
)
from ItemView import ItemView
from OrderView import OrderView
import sys
from DatabaseOperation import DatabaseOperation

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        connection_str = "mongodb+srv://Regnum771:Regnum771@cluster0.wewjs.mongodb.net/shop?retryWrites=true&w=majority"
        self.dbo = DatabaseOperation(connection_str)

        self.title = 'Item Panel'
        self.init_gui()
    
    def init_gui(self):
        #Layout Management
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QVBoxLayout(self.window)
        self.window.setLayout(self.layout)

        self.itemPanel = ItemView(self.dbo, self)
        self.itemPanel_button = QPushButton(self)
        self.itemPanel_button.setText("Item Panel")
        self.itemPanel_button.clicked.connect(self.openItemPanel)
        self.layout.addWidget(self.itemPanel_button)

        self.orderPanel = OrderView(self.dbo, self)
        self.orderPanel_button = QPushButton(self)
        self.orderPanel_button.setText("Order Panel")
        self.orderPanel_button.clicked.connect(self.openOrderPanel)
        self.layout.addWidget(self.orderPanel_button)

    def openItemPanel(self):
        self.itemPanel.show()

    def openOrderPanel(self):
        self.orderPanel.show()
    
    def closeEvent(self, event):
        self.dbo.close_client()

def main():
    app = QApplication()       
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()