
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QMainWindow, 
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget,
    QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QPushButton, 
    QDialog, QMessageBox, 
)

class ItemView(QMainWindow):
    def __init__(self, dbo, parent = None):
        super(ItemView, self).__init__(parent)
        self.dbo = dbo
        self.parent = parent

        self.title = 'Item View'
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle(self.title)

        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        self.item_panel = ItemPanel(self.dbo, self)
        self.layout.addWidget(self.item_panel)

    def closeEvent(self, event):
        self.item_panel.updateInfo()

class ItemPanel(QWidget):
    def __init__(self, dbo, parent = None):
        super(ItemPanel, self).__init__(parent)
        self.dbo = dbo
        self.parent = parent
        self.init_gui()

    def init_gui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        item_table = self.init_item_table()
        input_fields = self.init_input_fields()
        control_pallete = self.init_control_pallete()
        self.init_pop_up()

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addLayout(input_fields)
        wrapper_layout.setAlignment(input_fields, Qt.AlignTop)
        wrapper_layout.addLayout(control_pallete)
        wrapper_layout.setAlignment(control_pallete, Qt.AlignRight)
        self.layout.addLayout(item_table)
        self.layout.addLayout(wrapper_layout)
    
    """ INITIALIZATION

    """
    def init_item_table(self):
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
        
        self.items_table.currentItemChanged.connect(self.load)

        item_table_layout.addWidget(self.items_table)
        return item_table_layout

    def init_input_fields(self):
        input_fields_layout = QGridLayout()
        # Input fields
        # Name
        self.item_name_textbox = QLineEdit(self)
             
        self.item_name_label = QLabel("Item Name: ", self)
        self.item_name_label.setBuddy(self.item_name_textbox)
        input_fields_layout.addWidget(self.item_name_label, 0, 0, 1, 1)
        input_fields_layout.addWidget(self.item_name_textbox, 0, 2, 1, 2)
        # Price
        self.item_price_textbox = QLineEdit(self)

        self.item_price_label = QLabel("Item Price: ", self)
        self.item_price_label.setBuddy(self.item_price_textbox)   
        input_fields_layout.addWidget(self.item_price_label, 1, 0, 1, 1)
        input_fields_layout.addWidget(self.item_price_textbox, 1, 2, 1, 2)
        # Category
        self.item_category_textbox = QLineEdit(self)

        self.item_category_label = QLabel("Item Category: ", self)
        self.item_category_label.setBuddy(self.item_category_textbox)
        input_fields_layout.addWidget(self.item_category_label, 2, 0, 1, 1)
        input_fields_layout.addWidget(self.item_category_textbox, 2, 2, 1, 2)
        
        return input_fields_layout

    def init_control_pallete(self):
        control_pallete_layout = QGridLayout()
        
        # Buttons #
        # Delete
        delete_button = QPushButton('Delete', self)
        delete_button.clicked.connect(self.delete)
        control_pallete_layout.addWidget(delete_button, 0, 0)    
        # New 
        new_button = QPushButton('New', self)
        new_button.clicked.connect(self.new)
        control_pallete_layout.addWidget(new_button, 0, 1)    

        # Reset
        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.reset)
        control_pallete_layout.addWidget(reset_button, 0, 2)    

        # Apply
        apply_button = QPushButton('Apply', self)
        apply_button.clicked.connect(self.apply)
        control_pallete_layout.addWidget(apply_button, 0, 3) 

        return control_pallete_layout   

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
            if self.dbo.delete_item(self.item["_id"]):
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
            self.item = self.dbo.item_document(
                self.item["_id"], item_name, item_price, item_category)
            
            try:
                self.dbo.update_item(self.item["_id"], self.item)

                self.items_dict[self.item["_id"]]["name"] = item_name
                self.items_dict[self.item["_id"]]["price"] = item_price
                self.items_dict[self.item["_id"]]["category"] = item_category
                self.items_table.currentItem().setText(item_name)
            except ValueError as e:
                self.error_message.setText(str(e))
                self.error_message.exec()
        else:
            self.item = self.dbo.item_document(
                "", item_name, item_price, item_category)
            
            try:
                inserted_item_id = str(self.dbo.insert_item(self.item))
                self.item["_id"] = inserted_item_id

                self.items_dict[inserted_item_id] = self.dbo.item_document(
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
            self.item = self.dbo.empty_item()
            self.item_name_textbox.setText("")
            self.item_price_textbox.setText("")
            self.item_category_textbox.setText("")

    def test(self):
        print("Signal Connected")

    def updateInfo(self):
        print("Updating Item Changes...")
        self.parent.items_dict = self.items_dict
