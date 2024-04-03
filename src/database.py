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

    def generate_svg(user_data, template_path, output_path):
        with open(template_path, 'r') as f:
            svg_template = f.read()

        # Replace placeholders with actual data
        svg_template = svg_template.replace('{{ user_level }}', str(user_data['user_level']))
        svg_template = svg_template.replace('{{ total_quests }}', str(user_data['total_quests']))
        svg_template = svg_template.replace('{{ power_ups }}', str(user_data['power_ups']))
        svg_template = svg_template.replace('{{ community_rating }}', str(user_data['community_rating']))

        # Save the updated SVG to a new file
        with open(output_path, 'w') as f:
            f.write(svg_template)

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
            # Generate SVG file for the new user
            template_path = '..\userCards\template.svg'
            output_path = f'..\userCards\{user_name}_stats.svg'  
            self.generate_svg(new_user['user_data'], template_path, output_path)
            print("User created successfully.")
            print("User stats written to SVG file.")
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

