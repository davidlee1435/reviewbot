import re
import datetime
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.reviewbot
reviews_collection = db.reviews

def create_review(user, command, channel):
    pr_url = _extract_pr_url(command)
    print "Creating review for {0} from user {1}".format(pr_url, user)
    if not pr_url:
        return
    review = {'reviewee_id': user,
              'reviewer_id': None,
              'url': pr_url,
              'created_at': datetime.datetime.utcnow()}
    review_id = reviews_collection.insert_one(review).inserted_id
    return review_id

def _extract_pr_url(command):
    words = command.split()
    url = [word for word in words if "github.com" in word and "/pull/" in word]
    if not url:
        print "Url not in command!"
        return
    return url[0]

def get_review(review_id):
    return reviews_collection.find_one({"_id": review_id})
