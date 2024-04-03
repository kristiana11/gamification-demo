from pymongo.mongo_client import MongoClient
from pymongo import errors
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

    def create_user(self, user_name):
        print(f"Creating user: {user_name}.")
        new_user = dict()
        new_user['_id'] = user_name
        new_user['user_data'] = {
            'user_level': 1,  # Initial user level
            'total_quests': 0,  # Initial total quests completed
            'power_ups': 0,  # Initial power-ups used
            'community_rating': 0  # Initial community rating
        }
        try:
            self.collection.insert_one(new_user)
        except errors.DuplicateKeyError:
            print("User already exists!")

    def update_data(self, user_data):
        filter_query = {"_id": user_data["_id"]}
        update_query = {"$set": user_data}
        self.collection.update_one(filter_query, update_query, upsert=True)

    def download_user_data(self, user):
        user_document = self.collection.find_one({'_id': user})
        return user_document
    
    def get_user_stats(self, user):
        user_document = self.download_user_data(user)
        if user_document:
            return user_document['user_data']
        else:
            return None

