from pymongo import MongoClient, GEOSPHERE, ASCENDING
import logging
import functools

import os
from dotenv import load_dotenv
# Load Environment Variables
load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME') or 'taxi_fleet'

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
        if DB_NAME not in db_names:
            logging.info("Database not present, creating a database")
        else:
            db_client[DB_NAME]
            logging.info("Database created")
        self.database = db_client[DB_NAME]

    def get_collection(self, name):
        # improve error handling later
        return self.database[name]

    def _remove_internal_data(self, document):
        if document:
            document.pop("_id", None)
            return document
        else:
            return document

    def get_all_records(self, collection):
        return [ self._remove_internal_data(rec) for rec in self.database[collection].find({}) ]


    def get_multiple_data(self, collection, key):
        db_collection = self.get_collection(collection)
        documents = db_collection.find(key)
        return [self._remove_internal_data(document) for document in documents]

    def get_single_data(self, collection, key):
        db_collection = self.get_collection(collection)
        document = db_collection.find_one(key)
        if document:# Object ID not serialized by jsonify by flask
            document.pop("_id", None)
        return document

    def insert_single_data(self, collection, data):
        db_collection = self.get_collection(collection)
        document = db_collection.insert_one(data)
        return document.inserted_id

    def insert_multiple_data(self, collection, data):
        db_collection = self.get_collection(collection)
        result = db_collection.insert_many(data)
        return result.inserted_ids
    
    
    
    def delete_single_data(self, collection, key):
        db_collection = self.get_collection(collection)
        result = db_collection.delete_one(key)
        return result.deleted_count > 0
    
    def update_single_data(self, collection, key, data):
        db_collection = self.get_collection(collection)
        update_query = {"$set": data}
        document = db_collection.update_one(key, update_query)
        return document
    
    def count_documents(self, collection, key):
        db_collection = self.get_collection(collection)
        document = db_collection.count_documents(key)
        return document
    
    def paginated_list(self, collection, key, offset, limit):
        db_collection = self.get_collection(collection)
        document = db_collection.find(key).skip(offset).limit(limit)
        return document
    
    def replace_one(self, collection, key, data):
        db_collection = self.get_collection(collection)
        document = db_collection.replace_one(key,data, upsert = True)
        return document.upserted_id
    
    def create_geo_index(self, collection, column_name):
        db_collection = self.get_collection(collection)
        db_collection.create_index([(column_name, GEOSPHERE)])
        #db_collection.create_index([(column_name, '2D')])

    def check_index_exists(self, collection, index_name):
        db_collection = self.get_collection(collection)
        index_info = db_collection.index_information()
        return index_name in index_info

    def create_unique_index(self, collection, column_name):
        db_collection = self.get_collection(collection)
        if self.check_index_exists(collection, column_name) is False:
            db_collection.create_index([(column_name, ASCENDING)], unique=True)