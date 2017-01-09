import re
import datetime
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.reviewbot
reviews_collection = db.reviews

def create_review(user, command, channel):
    print "Creating review from " + command
    pr_url = extract_pr_url(command)
    print pr_url
    review = {'reviewee': user,
              'reviewer': None,
              'url': pr_url,
              'created_at': datetime.datetime.utcnow()}
    review_id = reviews_collection.insert_one(review).inserted_id
    print reviews_collection.find_one({'reviewee': user})
    return review_id

def extract_pr_url(command):
    words = command.split()
    url = [word for word in words if "github.com" in word]
    if not url:
        return None
    return url[0]
