from pymongo import MongoClient
import logging
import functools

DB_HOST = "127.0.0.1"
DB_PORT = "27017"
DB_NAME = "taxi_fleet"

class Singleton(object):
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

class Database(Singleton):

    def __init__(self):
        db_client = MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')
        db_names = db_client.list_database_names()
        if DB_NAME in db_names:
            logging.info("Database not present, creating a database")
        else:
            db_client[DB_NAME]
            logging.info("Database created")
        self.database = db_client[DB_NAME]

    def get_collection(self, name):
        # improve error handling later
        return self.database[name]

    def get_single_data(self, collection, key):
        db_collection = self.get_collection(collection)
        document = db_collection.find_one(key)
        return document

    def get_multiple_data(self, collection, key):
        db_collection = self.get_collection(collection)
        documents = db_collection.find(key)
        return documents

    def insert_single_data(self, collection, data):
        db_collection = self.get_collection(collection)
        document = db_collection.insert_one(data)
        return document.inserted_id

    def insert_multiple_data(self, collection, data):
        db_collection = self.get_collection(collection)
        result = db_collection.insert_many(data)
        return result.inserted_ids
    
    def get_all_records(self, collection):
        return self.database[collection].find({})

    def update_single_data(self, collection, key_filter, key_update):
        db_collection = self.get_collection(collection)
        document = db_collection.update_one(key_filter,key_update)
        return document.upserted_id

    def count_documents(self, collection, key):
        db_collection = self.get_collection(collection)
        document = db_collection.count_documents(key)
        return document