from PySide6.QtCore import Signal, Qt, QEvent
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import (
    QMainWindow, 
    QHBoxLayout, QVBoxLayout, QGridLayout, 
    QWidget, QMenu, 
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QDialog, QComboBox, QSizePolicy
)

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
        
    def onClick(self):
        self.ITEM_SELECTED.emit(self.item_id)
    
    def getButtonId(self):
        return self.button_id
    
    def getItemId(self):
        return self.item_id

    def setItem(self, item_id, item_name):
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

class OrderView(QMainWindow):
    def __init__(self, dbo, parent = None):
        super(OrderView, self).__init__(parent)
        self.dbo = dbo

        self.title = 'Order Panel'
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(self.title)
        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        self.button_panel = ButtonPanel(self.dbo, self)
        self.order_panel = OrderPanel(self.dbo, self)
        self.layout.addWidget(self.button_panel)
        self.layout.addWidget(self.order_panel)
    def closeEvent(self, event):
        self.button_panel.saveLayout()

class ButtonPanel(QWidget):
    def __init__(self, dbo, parent = None):
        super(ButtonPanel, self).__init__(parent)
        self.dbo = dbo
        self.item_dict = self.dbo.read_all_items(sort = "name")
        self.button_layout_dict = self.dbo.read_button_layout()
        self.buttons = []

        # Appearance Setting
        self.init_gui()
        
    def init_gui(self):
        #Layout Management
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Custom Context Menu
        self.button_menu = QMenu(self)

        button_config_action = QAction("Set Item", self.button_menu)
        button_config_action.triggered.connect(self.onItemConfigAction)

        self.button_menu.addAction(button_config_action)
        # Button Layout
        self.selected_button = None
        self.initSavedItems()

        # Button Configuration Dialog
        self.button_config_dialog = QDialog(self)
        button_config_dialog_layout = QHBoxLayout()
        self.button_config_dialog.setLayout(button_config_dialog_layout)

        self.item_selection_comboBox = QComboBox(self.button_config_dialog)

        i = 0
        for key, value in self.item_dict.items():
            self.item_selection_comboBox.addItem(value["name"])
            self.item_selection_comboBox.setItemData(i, key, Qt.UserRole + 1)
            i += 1
        
        button_config_dialog_layout.addWidget(self.item_selection_comboBox)

        change_dialog_discard_button = QPushButton(self.button_config_dialog)
        change_dialog_discard_button.setText("Save")
        change_dialog_discard_button.clicked.connect(self.onItemConfigSave)
        button_config_dialog_layout.addWidget(change_dialog_discard_button)

    def initEmptyGrid(self, rowSpan, columnSpan):
        for i in range(rowSpan):
            for j in range(columnSpan):
                button = QPushButton("")
                self.layout.addWidget(button, i, j, 1, 1)

    def initSavedItems(self):
        for key, value in self.button_layout_dict.items():
            button_id = key
            row = value["row"]
            col = value["column"]
            item_id = value["item_id"]

            if item_id in self.item_dict:
                item_name = self.item_dict[item_id]["name"]
            else:
                item_name = "EMPTY"

            button = Button(button_id, item_id, item_name, self)
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(self.onContextMenu)
            
            self.layout.addWidget(button, row, col, 1, 1)
            self.buttons.append(button)
    
    # Slot
    def onContextMenu(self, point):
        self.button_menu.exec(QCursor.pos())
    
    def onItemConfigAction(self, s):
        self.button_config_dialog.exec()
    
    def onItemConfigSave(self):
        self.selected_button.setItem(
            self.item_selection_comboBox.currentData(Qt.UserRole + 1),
            self.item_selection_comboBox.currentText()
        )      
        self.button_config_dialog.close()

    def saveLayout(self):
        for button in self.buttons:
            self.button_layout_dict[button.getButtonId()]["item_id"] = button.getItemId()
        self.dbo.save_button_layout(self.button_layout_dict)

class OrderPanel(QWidget):
    def __init__(self, dbo, parent = None):
        super(OrderPanel, self).__init__(parent)
        self.dbo = dbo
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
        item_table_layout = QVBoxLayout()

        self.items_table = QTableWidget(100, 2, self)
        self.items_table.setHorizontalHeaderLabels(["Item Name"])
        self.items_table.setFixedWidth(150)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.hideColumn(1)

        self.items_dict = self.dbo.read_all_items(sort = "name")
        self.item = None
        self.row_count = 0
        
        # Fill the table with empty invisble items
        for i in range(100):
            item_name_widget = QTableWidgetItem("")
            item_id_widget = QTableWidgetItem("")
            item_name_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)
            item_id_widget.setFlags(Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled)
            self.items_table.setItem(self.row_count, 0, item_name_widget)
            self.items_table.setItem(self.row_count, 1, item_id_widget)
            self.items_table.hideRow(self.row_count)
            self.row_count += 1

        # Fill the table with items from the database
        self.row_count = 0
        for key, item in self.items_dict.items():
            item_name_widget = self.items_table.item(self.row_count, 0)
            item_name_widget.setText(item["name"])
            
            item_id_widget = self.items_table.item(self.row_count, 1)
            item_id_widget.setText(key)

            self.items_table.showRow(self.row_count)
            self.row_count += 1
        
        #self.items_table.currentItemChanged.connect(self.load)

        item_table_layout.addWidget(self.items_table)
        return item_table_layout

    def init_control_pallete(self):
        control_pallete_layout = QGridLayout()
        
        total_button = QPushButton('Total', self)
        total_button.clicked.connect(self.total)
        control_pallete_layout.addWidget(total_button, 0, 0)    

        tender_button = QPushButton('Tender', self)
        tender_button.clicked.connect(self.tender)
        control_pallete_layout.addWidget(tender_button, 0, 1) 
              
        return control_pallete_layout

    def total(self):
        return 0

    def tender(self):
        return 0