from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QWidget,
    QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QPushButton, 
    QDialog, QMessageBox)
from bson.objectid import ObjectId
import DatabaseOperation as dbo

class ItemView(QMainWindow):
    def __init__(self, parent = None):
        super(ItemView, self).__init__(parent)
        self.parent = parent

        self.title = 'Item View'
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        self.item_panel = ItemPanel(self)
        self.layout.addWidget(self.item_panel)

    def closeEvent(self, event):
        self.item_panel.updateInfo()

class ItemPanel(QWidget):
    def __init__(self, parent = None):
        super(ItemPanel, self).__init__(parent)
        self.parent = parent
        self.init_gui()

    def init_gui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.init_item_table()
        self.init_input_fields()
        self.init_control_pallete()
        self.init_pop_up()

    """ INITIALIZATION

    """
    def init_item_table(self):
        self.item = None
        self.items_dict = dbo.read_all_items(sort = "name")
        self.items_table = QTableWidget(100, 2, self)
        self.row_count = 0
        #Populate empty table
        for i in range(100):
            item_name_widget = QTableWidgetItem("")
            item_id_widget = QTableWidgetItem("")
            item_name_widget.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                QtCore.Qt.ItemFlag.ItemIsEnabled)
            item_id_widget.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.items_table.setItem(self.row_count, 0, item_name_widget)
            self.items_table.setItem(self.row_count, 1, item_id_widget)
            self.items_table.hideRow(self.row_count)
            self.row_count += 1

        #Reset row count
        self.row_count = 0
        for key, item in self.items_dict.items():
            item_name_widget = self.items_table.item(self.row_count, 0)
            item_name_widget.setText(item["name"])
            
            item_id_widget = self.items_table.item(self.row_count, 1)
            item_id_widget.setText(key)

            self.items_table.showRow(self.row_count)
            self.row_count += 1
        self.items_table.hideColumn(1)

        self.items_table.move(20, 20)
        self.items_table.resize(200, 560)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.setHorizontalHeaderLabels(["Item Name"])
        self.items_table.currentItemChanged.connect(self.load)

    def init_input_fields(self):
        # Input fields
        # Name
        self.item_name_textbox = QLineEdit(self)
        self.item_name_textbox.move(400, 20)

        self.item_name_label = QLabel("Item Name: ", self)
        self.item_name_label.move(300, 20)
        self.item_name_label.setBuddy(self.item_name_textbox)

        # Price
        self.item_price_textbox = QLineEdit(self)
        self.item_price_textbox.move(400, 60)

        self.item_price_label = QLabel("Item Price: ", self)
        self.item_price_label.move(300, 60)
        self.item_price_label.setBuddy(self.item_price_textbox)   
        
        # Category
        self.item_category_textbox = QLineEdit(self)
        self.item_category_textbox.move(400, 100)

        self.item_category_label = QLabel("Item Category: ", self)
        self.item_category_label.move(300, 100)
        self.item_category_label.setBuddy(self.item_category_textbox)   

    def init_control_pallete(self):
        # Buttons #
        # Delete
        self.load_button = QPushButton('Delete', self)
        self.load_button.move(350, 550)
        self.load_button.clicked.connect(self.delete)

        # New 
        self.load_button = QPushButton('New', self)
        self.load_button.move(450, 550)
        self.load_button.clicked.connect(self.new)

        # Reset
        self.load_button = QPushButton('Reset', self)
        self.load_button.move(550, 550)
        self.load_button.clicked.connect(self.reset)

        # Apply
        self.apply_button = QPushButton('Apply', self)
        self.apply_button.move(650, 550)
        self.apply_button.clicked.connect(self.apply)

    def init_pop_up(self):
        # Dialog #
        # On Item Changed Dialog
        self.change_dialog = QDialog(self)
        self.change_dialog.setFixedSize(400, 100)

        change_dialog_discard_button = QPushButton(self.change_dialog)
        change_dialog_discard_button.setText("Discard Changes")
        change_dialog_discard_button.move(50, 50)
        change_dialog_discard_button.clicked.connect(self.change_dialog.close)
        change_dialog_discard_button.clicked.connect(self.reset)

        change_dialog_keep_button = QPushButton(self.change_dialog)
        change_dialog_keep_button.setText("Keep Changes")
        change_dialog_keep_button.move(150, 50)
        change_dialog_keep_button.clicked.connect(self.change_dialog.close)
        change_dialog_keep_button.clicked.connect(self.apply)
        
        # Error Message Box
        self.error_message = QMessageBox(self)
        self.error_message.setFixedSize(400, 100)
    """ BUTTON SLOTS

    """
    def delete(self):
        if not self.item["_id"]:
            self.items_table.removeRow(self.items_table.currentRow())
        else:    
            if dbo.delete_item(self.item["_id"]):
                self.items_dict.pop(self.item["_id"]) 
                self.items_table.removeRow(self.items_table.currentRow())
                self.row_count -= 1

    def new(self):
        self.items_table.showRow(self.row_count)
        self.items_table.setCurrentCell(self.row_count, 0)

    def reset(self):
        if self.item:
            self.item_name_textbox.setText(self.item["name"])
            self.item_price_textbox.setText(str(self.item["price"]))
            self.item_category_textbox.setText(",".join(self.item["category"]))
        else: 
            self.item_name_textbox.setText("")
            self.item_price_textbox.setText("")
            self.item_category_textbox.setText("")

    def apply(self):
        item_name = self.item_name_textbox.text()
        item_price = self.item_price_textbox.text()
        item_category = self.item_category_textbox.text().split(",")

        if self.item["_id"]:
            self.item = dbo.item_document(
                self.item["_id"], item_name, item_price, item_category)
            
            try:
                dbo.update_item(self.item["_id"], self.item)

                self.items_dict[self.item["_id"]]["name"] = item_name
                self.items_dict[self.item["_id"]]["price"] = item_price
                self.items_dict[self.item["_id"]]["category"] = item_category
                self.items_table.currentItem().setText(item_name)
            except ValueError as e:
                self.error_message.setText(str(e))
                self.error_message.exec()
        else:
            self.item = dbo.item_document(
                "", item_name, item_price, item_category)
            
            try:
                inserted_item_id = str(dbo.insert_item(self.item))
                self.item["_id"] = inserted_item_id

                self.items_dict[inserted_item_id] = dbo.item_document(
                    inserted_item_id, item_name, item_price, item_category
                )

                self.items_table.item(self.row_count, 0).setText(item_name)
                self.items_table.item(self.row_count, 1).setText(inserted_item_id)

                self.row_count += 1               
            except ValueError as e:
                self.error_message.setText(str(e))
                self.error_message.exec()

    """ TABLE SLOT   

    """
    def load(self, current, previous):
        # Detects unsaved changes
        if self.item:
            if self.item["name"] != self.item_name_textbox.text():
                self.items_table.blockSignals(True)
                self.items_table.setCurrentItem(previous)
                self.change_dialog.exec()
                self.items_table.setCurrentItem(current)
                self.items_table.blockSignals(False)

        # Fetch item data from item dictionary
        selected_item_id = self.items_table.item(current.row(), 1).text()
        if selected_item_id in self.items_dict:
            self.item = self.items_dict[selected_item_id]
            self.item_name_textbox.setText(self.item["name"])
            self.item_price_textbox.setText(str(self.item["price"]))
            if len(self.item["category"]) < 1:
                self.item_category_textbox.setText(
                    "".join(self.item["category"]))
            else:
                self.item_category_textbox.setText(
                    ",".join(self.item["category"]))
        else:    
            self.item = dbo.empty_item()
            self.item_name_textbox.setText("")
            self.item_price_textbox.setText("")
            self.item_category_textbox.setText("")

    def test(self):
        print("Signal Connected")

    def updateInfo(self):
        print("Updating Item Changes...")
        self.parent.items_dict = self.items_dict
