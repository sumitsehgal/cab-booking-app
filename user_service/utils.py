from pymongo import MongoClient
import logging
import functools

from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

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
        # Object ID not serialized by jsonify by flask
        document.pop("_id", None)
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
    
    def delete_single_data(self, collection, key):
        db_collection = self.get_collection(collection)
        result = db_collection.delete_one(key)
        return result.deleted_count > 0
    
    def update_single_data(self, collection, key, data):
        db_collection = self.get_collection(collection)
        update_query = {"$set": data}
        document = db_collection.update_one(key, update_query)
        return document
    