from PySide6.QtWidgets import (
    QMainWindow, QWidget,           
    QVBoxLayout, 
    QPushButton,
)
from ItemView import ItemView
from OrderView import OrderView
class MainWindow(QMainWindow):
    def __init__(self, model, parent = None):
        super(MainWindow, self).__init__(parent)
        self.model = model
        self.title = 'Item Panel'
        self.init_gui()
    
    def init_gui(self):
        #Layout Management
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QVBoxLayout(self.window)
        self.window.setLayout(self.layout)

        self.itemPanel = ItemView(self.model, self)
        self.itemPanel_button = QPushButton(self)
        self.itemPanel_button.setText("Item Panel")
        self.itemPanel_button.clicked.connect(self.openItemPanel)
        self.layout.addWidget(self.itemPanel_button)

        self.orderPanel = OrderView(self.model, self)
        self.orderPanel_button = QPushButton(self)
        self.orderPanel_button.setText("Order Panel")
        self.orderPanel_button.clicked.connect(self.openOrderPanel)
        self.layout.addWidget(self.orderPanel_button)

    def openItemPanel(self):
        self.itemPanel.show()

    def openOrderPanel(self):
        self.orderPanel.show()
    
    def closeEvent(self, event):
        self.itemPanel.closeEvent(event)
        self.orderPanel.closeEvent(event)
