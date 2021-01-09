from pymongo import MongoClient
import datetime

class dbMonger:
    def __init__(self, address, dbName, collection):
        self.client = MongoClient()
        self.client = MongoClient(address)
        self.mydatabase = self.client[dbName]
        self.collection = collection

    def search(self, obj):
        searchObj = self.mydatabase[self.collection].find_one(obj)
        if searchObj is not None:
            return searchObj
        else:
            return False

    def insert(self, row):
        rec = self.mydatabase[self.collection].insert(row)
        return row

    def update(self, oldObject, newObject):
        self.mydatabase[self.collection].update_one(oldObject, {"$set": newObject})

    def listAll(self, search={}):
        return self.mydatabase[self.collection].find(search)