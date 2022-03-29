from time import strftime
from PySide6.QtCore import Signal, Qt, QEvent, QSize
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import (
    QMainWindow, 
    QHBoxLayout, QVBoxLayout, QGridLayout, 
    QWidget, QMenu, 
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QDialog, QComboBox, QSizePolicy, QHeaderView
)
from datetime import datetime

class OrderView(QMainWindow):
    def __init__(self, model, parent = None):
        super(OrderView, self).__init__(parent)
        self.parent = parent
        self.model = model

        self.title = "Order View"
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(self.title)
        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        self.order_panel = OrderPanel(self.model, self)
        self.button_panel = ButtonPanel(self.model, self)
        self.layout.addWidget(self.button_panel)
        self.layout.addWidget(self.order_panel)

    def closeEvent(self, event):
        self.model.save_button_layout()

class ButtonPanel(QWidget):
    def __init__(self, model, parent = None):
        super(ButtonPanel, self).__init__(parent)
        self.parent = parent
        self.model = model
        self.selected_button = None

        self.init_gui()
        self.init_button_layout()
        
    def init_gui(self):
        #Layout Management
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Custom Context Menu
        self.button_context_menu = QMenu(self)

        button_config_action = QAction("Set Item", self.button_context_menu)
        button_config_action.triggered.connect(self.init_button_config_dialog)
        self.button_context_menu.addAction(button_config_action)

        clear_button_config_action = QAction("Clear", self.button_context_menu)
        clear_button_config_action.triggered.connect(self.clear_button_config)
        self.button_context_menu.addAction(clear_button_config_action)

        # Button Configuration Dialog
        config_dialog_layout = QHBoxLayout()
        self.button_config_dialog = QDialog(self)
        self.button_config_dialog.setLayout(config_dialog_layout)

        self.item_selection_comboBox = QComboBox(self.button_config_dialog)
        i = 0
        for key, value in self.model.item_dict.items():
            self.item_selection_comboBox.addItem(value["name"])
            self.item_selection_comboBox.setItemData(i, key, Qt.UserRole + 1)
            i += 1

        save_config_button = QPushButton("Save", self.button_config_dialog)
        save_config_button.clicked.connect(self.save_button_config)

        config_dialog_layout.addWidget(self.item_selection_comboBox)
        config_dialog_layout.addWidget(save_config_button)

    def init_button_layout(self):
        for key, value in self.model.button_layout_dict.items():
            button_id = key
            row = value["row"]
            col = value["column"]
            item_id = value["item_id"]

            if item_id in self.model.item_dict:
                item_name = self.model.item_dict[item_id]["name"]
            else:
                item_name = "EMPTY"

            button = Button(button_id, item_id, item_name, self)
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(self.init_context_menu)
            button.ITEM_SELECTED.connect(self.parent.order_panel.add_item_to_order)

            self.layout.addWidget(button, row, col, 1, 1)
    
    def clear_button_config(self):
        self.selected_button.set_item("", "EMPTY")
        self.model.button_layout_dict[self.selected_button.get_button_id()]["item_id"] = ""
    # Slot
    def init_context_menu(self, point):
        self.button_context_menu.exec(QCursor.pos())
    
    def init_button_config_dialog(self, s):
        self.button_config_dialog.exec()
    
    def save_button_config(self):
        self.selected_button.set_item(
            self.item_selection_comboBox.currentData(Qt.UserRole + 1),
            self.item_selection_comboBox.currentText()
        )      
        self.model.button_layout_dict[self.selected_button.get_button_id()]["item_id"] = self.selected_button.get_item_id()
        self.button_config_dialog.close()

class OrderPanel(QWidget):
    def __init__(self, model, parent = None):
        super(OrderPanel, self).__init__(parent)
        self.model = model

        self.order_total = 0
        self.row_count = 0
        self.current_order = {
            "date":"",
            "time":"",
            "order_details":{},
            "total":""
        }
        
        # Appearance Setting 
        self.init_gui()

    def init_gui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        order_detail_panel = self.init_order_detail_panel()
        control_pallete_layout = self.init_control_pallete()

        self.layout.addLayout(order_detail_panel)
        self.layout.addLayout(control_pallete_layout)

        self.layout.setAlignment(order_detail_panel, Qt.AlignTop)
        self.layout.setAlignment(control_pallete_layout, Qt.AlignBottom)
  
    def init_order_detail_panel(self):
        self.item_table = QTableWidget(100, 4, self)
        item_table_layout = QVBoxLayout()
        item_table_layout.addWidget(self.item_table)

        # Fill the table with empty invisble items
        for i in range(100):
            item_name_widget = QTableWidgetItem("")
            item_price_widget = QTableWidgetItem("0")
            item_quantity_widget = QTableWidgetItem("0")
            item_total_widget = QTableWidgetItem("0")

            item_name_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)
            item_price_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)
            item_quantity_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)
            item_total_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)

            self.item_table.setItem(self.row_count, 0, item_name_widget)
            self.item_table.setItem(self.row_count, 1, item_price_widget)
            self.item_table.setItem(self.row_count, 2, item_quantity_widget)
            self.item_table.setItem(self.row_count, 3, item_total_widget)

            self.item_table.hideRow(self.row_count)
            self.row_count += 1
        self.item_table.showRow(0)
        self.row_count = 0

        self.item_table.setHorizontalHeaderLabels(
            ["Item Name", "Price", "Qty", "Total"])
        self.item_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.item_table.setFixedWidth(400)
        self.item_table.setColumnWidth(0, 200)
        self.item_table.setColumnWidth(1, 50)
        self.item_table.setColumnWidth(2, 50)
        self.item_table.setColumnWidth(3, 50)

        return item_table_layout

    def init_control_pallete(self):
        control_pallete_layout = QGridLayout()
        
        total_button = QPushButton('Total', self)
        total_button.clicked.connect(self.total)
        control_pallete_layout.addWidget(total_button, 0, 0)    

        clear_button = QPushButton('Clear', self)
        clear_button.clicked.connect(self.clear_order)
        control_pallete_layout.addWidget(clear_button, 0, 1) 
              
        return control_pallete_layout

    def add_item_to_order(self, item_id):
        price = 0
        if item_id in self.model.item_dict:
            price = self.model.item_dict[item_id]["price"]
            self.item_table.item(self.row_count, 0).\
                setText(self.model.item_dict[item_id]["name"])
            self.item_table.item(self.row_count, 1).\
                setText(str(price))
            self.item_table.item(self.row_count, 2).\
                setText("1")
            self.item_table.item(self.row_count, 3).\
                setText(str(price))
            self.row_count += 1
            self.item_table.showRow(self.row_count)
        if item_id in self.current_order["order_details"]:
            self.current_order["order_details"][item_id]["quantity"] += 1
            self.current_order["order_details"][item_id]["total"] += price
        else:
            self.current_order["order_details"][item_id] = {
                "item_id": item_id, "quantity":1, "total":price
                }
        self.order_total += price

    def total(self):
        date_time = datetime.now()
        
        # Set 
        self.current_order["date"] = date_time.strftime("%d/%m/%Y")
        self.current_order["time"] = date_time.strftime("%H:%M:%S")
        self.current_order["order_details"] = list(self.current_order["order_details"].values())
        self.current_order["total"] = self.order_total
        
        if self.model.insert_order(self.current_order):
            # clear table
            for i in range(self.row_count + 1):
                self.item_table.item(i, 0).setText("")
                self.item_table.item(i, 1).setText("0")
                self.item_table.item(i, 2).setText("0")
                self.item_table.item(i, 3).setText("0")

                self.item_table.hideRow(i)
            self.row_count = 0    
            self.item_table.showRow(0)

            # clear global variable
            self.order_total = 0
            self.current_order = self.current_order = {
                "date":"",
                "time":"",
                "order_details":{},
                "total":""
            }

    def clear_order(self):
        for i in range(self.row_count):
            self.item_table.item(i, 0).setText("")
            self.item_table.item(i, 1).setText("0")
            self.item_table.item(i, 2).setText("0")
            self.item_table.item(i, 3).setText("0")
            self.item_table.hideRow(i)
        self.row_count = 0  
        self.item_table.showRow(0)

        self.current_order = {
            "date":"",
            "time":"",
            "order_details":{},
            "total":""
        }

class Button(QPushButton):
    ITEM_SELECTED = Signal(str)

    def __init__(self, button_id, item_id, item_name, parent = None):
        super(Button, self).__init__(parent)
        self.parent = parent
        self.button_id = button_id
        self.item_id = item_id
        self.item_name = item_name
        self.setText(item_name)

        #self.clicked.connect(self.onClick)
        self.installEventFilter(self)

        self.setFixedSize(100, 100)
        
    def get_button_id(self):
        return self.button_id
    
    def get_item_id(self):
        return self.item_id

    def set_item(self, item_id, item_name):
        self.item_id = item_id
        self.item_name = item_name
        self.setText(item_name)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.parent.selected_button = self
            elif event.button() == Qt.LeftButton:
                self.ITEM_SELECTED.emit(self.item_id)
        return super().eventFilter(source, event)
