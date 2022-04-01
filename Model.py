class Model(object):
    def __init__(self, dbo):
        self.dbo = dbo
        self.item_dict = self.dbo.read_all_items(sort = "name")
        self.button_layout_dict = self.dbo.read_button_layout()

    def empty_item(self):
        return self.dbo.empty_item()

    def item_document(self, item_id = "", name = "", price = "", category = []):
        return self.dbo.item_document(item_id, name, price, category)
        
    def validate_item(self, item):
        if not item["name"]:
            raise ValueError("Item name cannot be empty")
        if not item["price"]:
            raise ValueError("Item Price cannot be empty")
        try:
            float(item["price"])
        except ValueError:
            raise ValueError("Item Price has to be a float")
        if float(item["price"]) < 0:
            raise ValueError("Item Price cannot be negative")
        
        document = {}
        document["name"] = item["name"]
        document["price"] = float(item["price"])
        document["category"] = item["category"]
        return document

    def insert_item(self, item):
        return self.dbo.insert_item(item)

    def read_one_item(self, item_id):
        return self.dbo.read_one_item(item_id)

    def read_all_items(self, sort = None):    
        return self.dbo.read_all_items(sort)

    def update_item(self, item_id, item):
        return self.dbo.update_item(item_id, item)

    def delete_item(self, item_id):
        return self.dbo.delete_item(item_id)

    def save_button_layout(self):
        for key, value in self.button_layout_dict.items():
            self.update_button(key, value["item_id"], value["style"])

    def update_button(self, button_id, new_item_id, style):
        return self.dbo.update_button(button_id, new_item_id, style)

    def insert_order(self, order):
        return self.dbo.insert_order(order)