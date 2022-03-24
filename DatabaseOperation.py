from enum import unique
from tokenize import Double
from turtle import pos
import pymongo
from pymongo import MongoClient
from pymongo.collation import Collation
from bson.objectid import ObjectId
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, 
    QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QWidget, QScrollArea,)
from PySide6.QtCore import QObject, Signal, Slot, QSize, Qt

client = pymongo.MongoClient("mongodb+srv://Regnum771:Regnum771@cluster0.wewjs.mongodb.net/shop?retryWrites=true&w=majority")

db = client["shop"]
orders = db["orders"]
items = db["items"]
button_layout = db["button_layout"]

def insert_document(collection, document):
    id = collection.insert_one(document).inserted_id
    return id

def delete_document(collection, id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result

def read_document(collection, query, sort = None):
    cursor = collection.find(query).\
            collation(Collation(locale="en")).\
            sort(sort, 1)
    result = {}
    for document in cursor:
        key = str(document["_id"])
        document["_id"] = key
        result[key] = document
    return result

def update_document(collection, query, document):
    result = collection.update_one(
        query, {"$set": document})
    return result

# Item Specific Operations
def empty_item():
    return {
        "_id":"",
        "name":"",
        "price":"",
        "category":[]
    }

def item_document(item_id = "", name = "", price = "", category = []):
    item_document = {
        "_id": item_id,
        "name": name,
        "price": price,
        "category": category
    }
    return item_document
    
def validate_item(item):
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

def insert_item(item):
    document = validate_item(item)
    id = insert_document(items, document)
    return id

def read_one_item(item_id):
    result = items.find_one({"_id": item_id})
    return result

def read_all_items(sort = None):    
    result = read_document(items, {}, sort)
    return result

def update_item(item_id, item):
    """
    Update existing document data by document ID
    :param document_id:
    :param data:
    :return:
    """
    document = validate_item(item)
    result = update_document(
        items, {'_id': ObjectId(item_id)}, document)
    return result.acknowledged

def delete_item(item_id):
    try:
        result = delete_document(items, item_id)
        return result.deleted_count
    except Exception as e:
        return str(e)

# Button Layout Specific Operations
def read_button_layout():
    return read_document(button_layout, {}, "row")

def save_button_layout(button_layout_dict):
    for key, value in button_layout_dict.items():
        update_button(key, value["item_id"])

def insert_button(button):
    id = insert_document(button_layout, button)
    return id

def update_button(button_id, new_item_id):
    result = update_document(
        button_layout, {"_id": ObjectId(button_id)}, {"item_id":new_item_id})
from enum import unique
from tokenize import Double
from turtle import pos
import pymongo
from pymongo import MongoClient
from pymongo.collation import Collation
from bson.objectid import ObjectId
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, 
    QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QWidget, QScrollArea,)
from PySide6.QtCore import QObject, Signal, Slot, QSize, Qt

client = pymongo.MongoClient("mongodb+srv://Regnum771:Regnum771@cluster0.wewjs.mongodb.net/shop?retryWrites=true&w=majority")

db = client["shop"]
orders = db["orders"]
items = db["items"]
button_layout = db["button_layout"]

def insert_document(collection, document):
    id = collection.insert_one(document).inserted_id
    return id

def delete_document(collection, id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result

def read_document(collection, query, sort = None):
    cursor = collection.find(query).\
            collation(Collation(locale="en")).\
            sort(sort, 1)
    result = {}
    for document in cursor:
        key = str(document["_id"])
        document["_id"] = key
        result[key] = document
    return result

def update_document(collection, query, document):
    result = collection.update_one(
        query, {"$set": document})
    return result

# Item Specific Operations
def empty_item():
    return {
        "_id":"",
        "name":"",
        "price":"",
        "category":[]
    }

def item_document(item_id = "", name = "", price = "", category = []):
    item_document = {
        "_id": item_id,
        "name": name,
        "price": price,
        "category": category
    }
    return item_document
    
def validate_item(item):
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

def insert_item(item):
    document = validate_item(item)
    id = insert_document(items, document)
    return id

def read_one_item(item_id):
    result = items.find_one({"_id": item_id})
    return result

def read_all_items(sort = None):    
    result = read_document(items, {}, sort)
    return result

def update_item(item_id, item):
    """
    Update existing document data by document ID
    :param document_id:
    :param data:
    :return:
    """
    document = validate_item(item)
    result = update_document(
        items, {'_id': ObjectId(item_id)}, document)
    return result.acknowledged

def delete_item(item_id):
    try:
        result = delete_document(items, item_id)
        return result.deleted_count
    except Exception as e:
        return str(e)

# Button Layout Specific Operations
def read_button_layout():
    return read_document(button_layout, {}, "row")

def save_button_layout(button_layout_dict):
    for key, value in button_layout_dict.items():
        update_button(key, value["item_id"])

def insert_button(button):
    id = insert_document(button_layout, button)
    return id

def update_button(button_id, new_item_id):
    result = update_document(
        button_layout, {"_id": ObjectId(button_id)}, {"item_id":new_item_id})
    return result