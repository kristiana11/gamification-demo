from pymongo.mongo_client import MongoClient
from pymongo import  errors
import os


class MongoDB:
    # TODO: implement config
    def __init__(self):
        self.uri = os.environ['MONGODB_URI']
        self.client = MongoClient(self.uri)
        self.db = self.client["gamification"]
        self.collection = self.db["user_data"]

    def close_connection(self):
        self.client.close()

    def dump_user_data(self, user_data):
        print("dumping to database:")
        print(user_data)
        try:
            self.collection.insert_one(user_data)
        except errors.DuplicateKeyError:
            self.collection.replace_one({'_id': user_data['_id']}, user_data, upsert=True)

    def read_user_data(self, user_data):
        user_document = self.collection.find_one({'_id': user_data['_id']})
        return user_document
