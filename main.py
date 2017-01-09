import os
import time
import random
import re
from slackclient import SlackClient
import mongo_helper as mh
import redis_helper as rh
import slack_helper as sh
# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

INTENTS = {
    'CLAIM_REVIEW': 0,
    'NOTIFY_REVIEWEE': 1
}

def outgoing_messages(intent, user, command, channel):
    if intent == INTENTS['CLAIM_REVIEW']:
        pass
    elif intent == INTENTS['NOTIFY_REVIEWEE']:
        pass
    else:
        return

def route_command(user, command, channel):
    if command.startswith('review'):
        response = "Your request has been received!"
    elif command.startswith('busy'):
        rh.set_user_availability(user, False)
        response = "Gotcha. You won't receive any requests"
    elif command.startswith('available'):
        rh.set_user_availability(user, True)
        response = "Cool! I'll let you know when there are PRs that need reviewing"
    else:
        response = "I didn't understand that. If you're busy, say 'busy'. If you're not busy, say 'not busy'. If you need a review, type 'review <url_to_github_PR>'"
    sh.post_message(channel, response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['user'], \
                       output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Reviewbot connected and running!")
        while True:
            user, command, channel = parse_slack_output(slack_client.rtm_read())
            if user and command and channel:
                print channel
                route_command(user, command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
