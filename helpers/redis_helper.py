# Stores all things that have to do with Redis
import redis
import os

r = redis.StrictRedis(host='localhost', port=6379, db=0)
BOT_ID = os.environ.get("BOT_ID")

def set_initial_user_statuses(users):
    for user in users:
        if user != 'USLACKBOT' and user != BOT_ID:
            set_user_availability(user, True)
    return

def set_user_availability(user, availability):
    """
    Sets the availability (ie. available to review a PR) of a given user
    """
    r.set(user, availability)

def find_available_users():
    """
    Returns a set of available users
    """
    available_users = set()
    user_ids = r.keys()
    for user in user_ids:
        if r.get(user) == 'True':
            available_users.add(user)
    return available_users
