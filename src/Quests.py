import requests
from sys import argv
from database import MongoDB
import json
import sys

db = MongoDB()


# accept quest
def accept_quest(user, quest):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)
    user_data = db.download_user_data(user)
    if quest in quests:
        if user_data['user_data'].get('accepted') is not None:
            if quest not in user_data['user_data']['accepted']:
                user_data['user_data']['accepted'] += [quest]
        else:
            user_data['user_data']['accepted'] = [quest]
    db.update_data(user_data)


def is_quest_accepted(user, quest):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)
    if quest in quests:
        user_data = db.download_user_data(user)
        if user_data['user_data'].get('accepted') is not None:
            if quest in user_data['user_data']['accepted']:
                sys.exit(0)  # success
    sys.exit(1)  # fail


# remove quest
def remove_quest(user, quest):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)
    if quest in quests:
        user_data = db.download_user_data(user)
        if user_data['user_data'].get('accepted') is not None:
            if quest in user_data['user_data']['accepted']:
                index = user_data['user_data']['accepted'].index(quest)
                del user_data['user_data']['accepted'][index]
        db.update_data(user_data)


def display_quests(user):
    response = ''
    # TODO: later implement a check for prerequisite met, prob a simple if statement with iterator
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)
    print("Available quests")
    user_data = db.download_user_data(user)
    if 'completed' in user_data['user_data']:
        completed_quests = user_data['user_data']['completed']
    else:
        completed_quests = []
    for quest in quests:
        if quest not in completed_quests:
            response += quest + ' '
    return 'available quests: ' + response


if __name__ == '__main__':
    user = argv[1]
    command = argv[2]
    if len(argv) == 4:
        quest = argv[3]
    # generate character
    if command == 'new':
        db.create_user(user)
    if command == 'accept':
        accept_quest(user, quest)
    if command == 'drop':
        remove_quest(user, quest)
    if command == 'display':
        print(display_quests(user))
    if command == 'check':
        is_quest_accepted(user, quest)
