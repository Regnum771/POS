from pymongo import MongoClient
from pymongo.collation import Collation
from bson.objectid import ObjectId

class DatabaseOperation:
    def __init__(self, username, password):
        connection_str = "mongodb+srv://" + username + ":" + password + "@cluster0.wewjs.mongodb.net/shop?retryWrites=true&w=majority"
        self.__client = MongoClient(connection_str)
        if self.__client is None:
            return
        db = self.__client["shop"]
        self.__orders = db["orders"]
        self.__items = db["items"]
        self.__button_layout = db["button_layout"]
    """PRIVATE
    
    """
    def __insert_document(self, collection, document):
        id = collection.insert_one(document).inserted_id
        return id

    def __delete_document(self, collection, id):
        result = collection.delete_one({"_id": ObjectId(id)})
        return result

    def __read_document(self, collection, query, sort = None):
        cursor = collection.find(query).\
                collation(Collation(locale="en")).\
                sort(sort, 1)
        result = {}
        for document in cursor:
            key = str(document["_id"])
            document["_id"] = key
            result[key] = document
        return result

    def __update_document(self, collection, query, document):
        result = collection.update_one(
            query, {"$set": document})
        return result

    """PUBLIC
    """
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
        document = self.validate_item(item)
        id = self.__insert_document(self.__items, document)
        return id

    def read_one_item(self, item_id):
        result = self.__items.find_one({"_id": item_id})
        return result

    def read_all_items(self, sort = None):    
        result = self.__read_document(self.__items, {}, sort)
        return result

    def update_item(self, item_id, item):
        """
        Update existing document data by document ID
        :param document_id:
        :param data:
        :return:
        """
        document = self.validate_item(item)
        result = self.__update_document(
            self.__items, {'_id': ObjectId(item_id)}, document)
        return result.acknowledged

    def delete_item(self, item_id):
        try:
            result = self.__delete_document(self.__items, item_id)
            return result.deleted_count
        except Exception as e:
            return str(e)

    # Button Layout Specific Operations
    def read_button_layout(self):
        return self.__read_document(self.__button_layout, {}, "row")

    def save_button_layout(self, button_layout_dict):
        for key, value in button_layout_dict.items():
            self.update_button(key, value["item_id"], value["style"])

    def insert_button(self, button):
        id = self.__insert_document(self.__button_layout, button)
        return id

    def update_button(self, button_id, new_item_id, style):
        result = self.__update_document(
            self.__button_layout, {"_id": ObjectId(button_id)}, {"item_id":new_item_id, "style":style})
        return result

    # Orders Specific Operations
    def insert_order(self, order):
        id = self.__insert_document(self.__orders, order)
        return id

    def close_client(self):
        self.__client.close()