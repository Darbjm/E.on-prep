import os
import re
import requests
import json
import time
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Define path of .env file
env_path = Path('.') / 'env'
load_dotenv(dotenv_path=env_path)
# initalizing app
app = App(
    token=os.environ["SLACK_TOKEN"],
    signing_secret=os.environ["SIGNING_SECRET"]
)
user_client = WebClient(os.environ["USER_TOKEN"])


def rate_limit(logger, methode, args=None, kwargs=None):
    '''Takes an api call as a method which might have a rate limit.
    This function allows the api call to be rerun if slack is too busy'''
    args = args or []
    kwargs = kwargs or {}
    try:
        response = methode(*args, **kwargs)
    except SlackApiError as e:
        logger.error(f"Error calling following {methode} message: {e}")
        if e.response["error"] == "ratelimited":
            # The `Retry-After` header will tell you how long to wait before
            # retrying
            delay = int(e.response.headers['Retry-After'])
            print(f"Rate limited. Retrying in {delay} seconds")
            time.sleep(delay)
            response = methode(*args, **kwargs)
        else:
            logger.error(f"Error calling following {methode} message: {e}")
            return e.response
    return response


def eph_message_block(text, ts, foward_ts, foward_channel):
    '''Function that sends an ephemeral message to the user and stores the channel
    and timestamp of the original message that triggered the epheremal
    message.'''
    two_ts = ts + ',' + foward_ts
    blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    },
        {
        "type": "actions",
        "block_id": foward_channel,
        "elements": [
            {
                "type": "button",
                "action_id": "delete",
                'value': two_ts,
                "style": "danger",
                "text": {
                    "type": "plain_text",
                    "text": "Delete my message"
                }
            },
            {
                "type": "button",
                "action_id": "ignore",
                'value': foward_ts,
                "text": {
                    "type": "plain_text",
                    "text": "Not the case"
                }
            }
        ]
    }]
    if text == "Please don't swear on public channels!":
        blocks.pop(1)
    return blocks


def foward_message(client, say, channel, ts, reason, post_to_channel, logger):
    # Create permalink for original message #
    # Gets hyperlink for offending message
    permalink = rate_limit(logger, client.chat_getPermalink, kwargs={
                           "channel": channel, "message_ts": ts})['permalink']
    # Message fowarded from bot #
    text = f'''{reason}\n The following link will take you to the original
    message: < {permalink} | *Show original message*>'''
    # try:
    # sends message to admins to review
    response = rate_limit(logger, say, kwargs={
                          "channel": post_to_channel, "text": text})
    # except:
    # response = create_channel(client, post_to_channel, say, text, logger)
    return response['ts'], response['channel']


def eph_message(message, client, say, text, post_to_channel, reason, logger):
    user = message['user']
    # Might be an API call we can do less
    # by getting the information else where.
    BOT_ID = client.api_call('auth.test')['user_id']
    if BOT_ID != user:
        channel = message['channel']
        ts = message['ts']
        foward_ts, foward_channel = foward_message(
            client, say, channel, ts, reason, post_to_channel, logger)
        blocks = eph_message_block(text, ts, foward_ts, foward_channel)
        rate_limit(logger, client.chat_postEphemeral, kwargs={
                   "channel": channel, "blocks": blocks, "user": user})


def delete_immediately(payload, logger):
    ts = payload['ts']
    original_channel = payload['channel']
    rate_limit(logger, user_client.chat_delete, kwargs={
        'channel': original_channel, 'ts': ts, 'as_user': True})


@app.message(re.compile(r'(?:^|\W)(fuck|fck|shit)(?:$|\W)', re.I))
def swear_message(ack, payload, client, message, say, logger):
    ack()
    private_mes_text = "Please don't swear on public channels!"
    post_to_channel = 'C01TJL6DV6K'
    reason = ':warning: :face_with_symbols_on_mouth: Bad language used :face_with_symbols_on_mouth: :warning:'
    eph_message(message, client, say, private_mes_text,
                post_to_channel, reason, logger)
    delete_immediately(payload, logger)


@app.event({
    "type": "message"
})
def message_deleted(ack):
    ack()


if __name__ == "__main__":
    app.start(5000)
