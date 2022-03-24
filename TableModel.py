from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication, QMainWindow, 
    QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QWidget, QScrollArea, QTableView, QItemDelegate)
from bson.objectid import ObjectId

from DatabaseOperation import read_item, insert_item, read_one_item, update_existing

class CustomModel(QtCore.QAbstractTableModel):
    def __init__(self, columns, data, parent=None):
        super(CustomModel, self).__init__(parent)
        self.columns = columns
        self.datatable = data
        self.datatable.append({key: None for key in self.columns if not key=='_id'})

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Edit data in table cells
        :param index:
        :param value:
        :param role:
        :return:
        """
        if index.isValid():
            selected_row = self.datatable[index.row()]
            selected_column = self.columns[index.column()]
            selected_row[selected_column] = value
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
            ok = update_existing(selected_row['_id'], selected_row)
            print(selected_row)
            if ok:
                return True
        return False

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section].title()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = self.datatable[index.row()]
            column_key = self.columns[index.column()]
            value = row[column_key]
            if isinstance(row[column_key], list):
                return ', '.join(value)
            return str(value)
        else:
            return None
    
    def insertRows(self):
        row_count = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), row_count, row_count)
        empty_data = { key: None for key in self.columns if not key=='_id'}
        document_id = insert_item(empty_data)
        new_data = read_one_item(document_id)
        self.datatable.append(new_data)
        self.endInsertRows()
        row_count += 1
        return True

    def flags(self, index):
        """
        Make table editable.
        make first column non editable
        :param index:
        :return:
        """
        if index.column() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif index.column() == 1:
            return QtCore.Qt.DecorationRole
        else:
            return QtCore.Qt.ItemIsSelectable

class InLineEditDelegate(QItemDelegate):
    """
    Delegate is important for inline editing of cells
    """
    def createEditor(self, parent, option, index):
        return super(InLineEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))

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

    
    window = MainWindow()
    
    model = CustomModel(["_id", "category", "name", "price",], read_item())

    table = QTableView()
    table.setModel(model)
    insert_item_button = QPushButton("Insert Item")
    insert_item_button.clicked.connect(model.insertRows)
       

    window.layout.addWidget(table)
    window.layout.addWidget(insert_item_button)

    window.show()
    return app.exec()

main()