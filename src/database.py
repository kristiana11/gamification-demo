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
            'xp': 0,
            'points': 0
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
    
# SVG file path
svg_file_path = 'userCards/draft.svg'

# Function to update SVG file with stats
def update_svg(stats):
    with open(svg_file_path, 'r') as file:
        svg_content = file.read()

    # Update stats in SVG content
    regex = r'>([^<]+)<\/text>\s+<text([^>]+)>(\d+)<\/text>'
    svg_content = re.sub(regex, lambda match: f'>{match.group(1)}<\/text><text{match.group(2)}>{stats[match.group(1).strip().lower().replace(" ", "")]}<\/text>', svg_content)

    # Write updated SVG content back to file
    with open(svg_file_path, 'w') as file:
        file.write(svg_content)

    print('SVG file updated with stats.')


# Function to fetch stats from MongoDB and update SVG
def fetch_stats_and_update_svg(user):
    # Connect to MongoDB
    mongo_client = MongoDB()

    try:
        # Fetch user data from MongoDB
        user_data = mongo_client.download_user_data(user)

        # Check if user data exists
        if user_data:
            # Update SVG with fetched stats
            update_svg(user_data['user_data'])
        else:
            print(f"User '{user}' not found.")
    except Exception as e:
        print('Error:', e)
    finally:
        # Close MongoDB connection
        mongo_client.close_connection()


# Call function to fetch stats and update SVG (replace 'username' with actual username)
fetch_stats_and_update_svg('{user}')
