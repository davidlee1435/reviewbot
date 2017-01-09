import os
from slackclient import SlackClient
import redis_helper
import mongo_helper
import review_service
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_all_users():
    response = slack_client.api_call('users.list')
    if response.get('ok'):
        return [member['id'] for member in response.get('members')]
    return []
    
def post_message(channel, message, as_user=True):
    slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user)

def create_notification_message(review):
    reviewee_id = review.get('reviewee_id')
    url = review.get('url')
    reviewee_name = "Someone"
    reviewee_info_response = slack_client.api_call("users.info", user=reviewee)
    if reviewee_info_response.get('ok'):
        reviewee_info = reviewee_info_response.get('user')
        reviewee_name = "@" + reviewee_info.get('name')
    return "{0} requested a PR: {1}".format(reviewee_info.get('name'))

def broadcast_new_review_notification(review, available_users):
    im_channels = slack_client.api_call('im.list')
    for channel in im_channels:
        if channel.get('user') in available_users:
            message = create_notification_message(review)
            slack_client.api_call('chat.postMessage',
                                  channel=channel,
                                  text=message,
                                  as_user=False)
    return
