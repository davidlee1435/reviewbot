# Stores all things that have to do with Redis
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def set_user_availability(user, availability):
    r.set(user, availability)

def find_available_users():
    available_users = []
    user_ids = r.keys()
    for user in user_ids:
        if r.get(user):
            available_users.append(user)
    return available_users
