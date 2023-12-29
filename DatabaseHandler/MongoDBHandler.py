from Interfaces.DatabaseHandler import DatabaseHandler
from pymongo import MongoClient
from Env.project_types import *
from Utils.file_handler import read_yaml
from Env.paths import CONFIG_PATH

class MongoDBHandler(DatabaseHandler):
    def __init__(self):
        
        configs = read_yaml(CONFIG_PATH + 'app_config.yaml')
        self.host = configs['databases']['local_mongodb']['host']
        self.port = configs['databases']['local_mongodb']['port']
        self.client = None

    def connect(self, db_name: str) -> None:
        
        self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
        self.db = self.client[db_name]      

    def disconnect(self):
        self.client.close()

    def write_data(self, collection_name: str, data: Documents) -> None:
        collection = self.db[collection_name]
        collection.insert_many(data)

    def read_data(self, collection_name: str , query: dict):
        collection = self.db[collection_name]
        return [doc for doc in collection.find(query) ] 