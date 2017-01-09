import os
from slackclient import SlackClient
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def post_message(channel, message, as_user=True):
    slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=as_user)
