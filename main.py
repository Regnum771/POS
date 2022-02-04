from pickle import TRUE
from tkinter import N

from PySide6.QtWidgets import (QApplication, QMainWindow, 
    QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QWidget, QScrollArea,)
from PySide6.QtCore import QObject, Signal, Slot, QSize, Qt
class Item:
    def __init__(self, name, price, column, row):
        self.name = name
        self.price = price
        self.column = column
        self.row = row

class Button(QWidget):
    ITEM_SELECTED = Signal(Item)

    def __init__(self, item):
        super().__init__()
        self.item = item
        button = QPushButton(self.item.name, self)
        button.clicked.connect(self.onClick)
        button.setFixedSize(100, 100)
        
        self.show()
        
    def onClick(self):
        self.ITEM_SELECTED.emit(self.item)

class ButtonPane(QWidget):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.buttons = []
        
        self.layout = QGridLayout(self)

        self.initEmptyGrid(4, 4)
        self.initSavedItems()

    def initEmptyGrid(self, rowSpan, columnSpan):
        for i in range(columnSpan):
            for j in range(rowSpan):
                button = QPushButton("")
                button.setFixedSize(100, 100)
                self.layout.addWidget(button, i, j, 1, 1)

    def initSavedItems(self):
        for item in self.items:
            button = Button(item)
            self.buttons.append(button)
            self.layout.addWidget(button, item.row, item.column)

    def connectButtonsToOrder(self, order):
        for button in self.buttons:
            button.ITEM_SELECTED.connect(order.addItemToOrder)

class OrderPane(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_main = QVBoxLayout(self)   
        self.layout_orderDetails = QVBoxLayout()
        self.layout_checkOut = QVBoxLayout()

        button_total =  QPushButton("TOTAL")
        button_tender = QPushButton("TENDER")
        button_total.clicked.connect(self.checkOut)
        self.layout_checkOut.addWidget(button_total)
        self.layout_checkOut.addWidget(button_tender)

        self.layout_main.addLayout(self.layout_orderDetails)
        self.layout_main.setAlignment(Qt.AlignBottom)     
        self.layout_main.addLayout(self.layout_checkOut)

        self.orderDetails = []

    def addItemToOrder(self, item):
        self.orderDetails.append(item)
        self.layout_orderDetails.addWidget(QPushButton(item.name))

    def checkOut(self):
        total = 0
        for item in self.orderDetails:
            total += item.price
        print("The total is: " + str(total))
        

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.init_gui()
    
    def init_gui(self):
        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

def main():
    app = QApplication()       

    #Will be read and constructed from a dictionary 
    items = [
        Item("apple", 1, 0, 0),
        Item("banana", 2, 1, 1),
        Item("citrus", 0, 0, 3),
        Item("dango", 0, 3, 0),
        Item("grape", 0, 3, 2),
        Item("japapeno", 0, 1, 3)
    ]
    window = MainWindow()
    buttonPane = ButtonPane(items)
    orderPane = OrderPane()
    orderPane2 = OrderPane()
    window.layout.addWidget(buttonPane)
    window.layout.addWidget(orderPane)

    buttonPane.connectButtonsToOrder(orderPane)

    window.show()
    return app.exec()

if __name__ == "__main__":
    main()