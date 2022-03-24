from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
    QPushButton,     
    QVBoxLayout)
from ItemView import ItemView
from OrderView import OrderView
import sys
import DatabaseOperation as dbo

print("This is new")

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Item Panel'
        #self.left = 50
        #self.top = 50
        #self.setFixedSize(800, 600)
        self.init_gui()
    
    def init_gui(self):
        #Layout Management
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QVBoxLayout(self.window)
        self.window.setLayout(self.layout)

        self.itemPanel = ItemView(self)
        self.itemPanel_button = QPushButton(self)
        self.itemPanel_button.setText("Item Panel")
        self.itemPanel_button.clicked.connect(self.openItemPanel)
        self.layout.addWidget(self.itemPanel_button)

        self.items_dict = dbo.read_all_items(sort = "name")
        button_layout_dict = dbo.read_button_layout()

        self.orderPanel = OrderView(self.items_dict, button_layout_dict, self)
        self.orderPanel_button = QPushButton(self)
        self.orderPanel_button.setText("Order Panel")
        self.orderPanel_button.clicked.connect(self.openOrderPanel)
        self.layout.addWidget(self.orderPanel_button)

    def openItemPanel(self):
        self.itemPanel.show()

    def openOrderPanel(self):
        self.orderPanel.show()

def main():
    app = QApplication()       
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()