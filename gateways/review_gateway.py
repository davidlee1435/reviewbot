import datetime
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.reviewbot
reviews_collection = db.reviews

def add_review(reviewee_id=None, reviewer_id=None, url=None):
    if not reviewee_id or not url:
        print "Must have reviewee and url"
        return None
    review = {'reviewee_id': reviewee_id,
              'reviewer_id': reviewer_id,
              'url': url,
              'created_at': datetime.datetime.utcnow()}
    review_id = reviews_collection.insert_one(review).inserted_id
    return review_id

def get_review(review_id=None):
    if not review_id:
        return
    return reviews_collection.find_one({"_id": review_id})
