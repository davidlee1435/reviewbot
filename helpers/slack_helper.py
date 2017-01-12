import os
from slackclient import SlackClient
import redis_helper
import mongo_helper
import review_service
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_all_users():
    response = slack_client.api_call('users.list')
    if response.get('ok'):
        return [member['id'] for member in response.get('members')]
    return []

def post_message(channel, message, as_user=True, link_names=1):
    slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user, link_names=link_names)

def create_notification_message(review):
    reviewee_id = review.get('reviewee_id')
    url = review.get('url')
    reviewee_name = "Someone"
    reviewee_info_response = slack_client.api_call("users.info", user=reviewee_id)
    if reviewee_info_response.get('ok'):
        reviewee_info = reviewee_info_response.get('user')
        reviewee_name = "@" + reviewee_info.get('name')
        print reviewee_name
    return "{0} requested a PR: {1}".format(reviewee_name, url)

def broadcast_new_review_notification(reviewee, review, available_users):
    im_channels = slack_client.api_call('im.list').get('ims')
    for channel in im_channels:
        channel_user = channel.get('user')
        if channel_user in available_users and channel_user != reviewee:
            message = create_notification_message(review)
            post_message(channel.get('id'), message, as_user=False)
    return
