import json

class User:
    def __init__(self):
        self.xp = 0
        self.data = dict()

    def load_user(self, user):
        try:
            with open(f"{user}Data.txt", "r") as user_data:
                self.data = json.load(user_data)
        except FileNotFoundError:
            print("No user data found.")

    def get_xp(self):
        self.xp = self.data['user_data']['xp']

