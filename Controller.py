class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def delete(self):
        if self.item["_id"]: 
            if self.model.delete_item(self.item["_id"]):
                self.items_dict.pop(self.item["_id"]) 
                self.items_table.removeRow(self.items_table.currentRow())
                #View
                self.error_message.setText("Item deleted successfully")
                self.row_count -= 1

    def new(self):
        #View
        self.items_table.showRow(self.row_count)
        self.items_table.setCurrentCell(self.row_count, 0)

    def reset(self):
        if self.item:
            #View
            self.item_name_textbox.setText(self.item["name"])
            self.item_price_textbox.setText(str(self.item["price"]))
            self.item_category_textbox.setText(",".join(self.item["category"]))
        else: 
            #View
            self.item_name_textbox.setText("")
            self.item_price_textbox.setText("")
            self.item_category_textbox.setText("")

    def apply(self):
        #View
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

                self.error_message.setText("Item inserted successfully")
                self.error_message.exec()

                self.row_count += 1
                self.items_table.showRow(self.row_count)
               
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