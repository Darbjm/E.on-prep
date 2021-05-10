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


# Define path of .env file #
env_path = Path('.') / 'bossy.env'
load_dotenv(dotenv_path=env_path)


# initalizing app #
app = App(
    token=os.environ["SLACK_TOKEN"],
    signing_secret=os.environ["SIGNING_SECRET"]
)
user_client = WebClient(os.environ["USER_TOKEN"])


# Functions #
# functions that delets the ephemeral message if the user clicks acknowledges
# the ephemeral message
def rate_limit(logger, methode, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or {}
    try:
        response = methode(*args, **kwargs)
    except SlackApiError as e:
        logger.error(f"Error calling following {methode} message: {e}")
        if e.response["error"] == "ratelimited":
            # The `Retry-After` header will tell you how long to wait
            # before retrying
            delay = int(e.response.headers['Retry-After'])
            print(f"Rate limited. Retrying in {delay} seconds")
            time.sleep(delay)
            response = methode(*args, **kwargs)
        else:
            logger.error(f"Error calling following {methode} message: {e}")
            return e.response
    return response


def delete_eph_message(body, logger):
    response_url = body['response_url']
    response = {
        'response_type': 'ephemeral',
        'text': '',
        'replace_original': True,
        'delete_original': True
    }
    rate_limit(logger, requests.post, args=[response_url], kwargs={
               "data": json.dumps(response)})


def eph_message_block(text, ts, foward_ts, foward_channel):
    two_ts = ts + ',' + foward_ts
    return [{
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
# Function that sends an ephemeral message to the user and stores the channel
# and ts of the original message that triggered the epheremal message
# def create_channel(client, post_to_channel, say, text, logger):
    # response = rate_limit(logger, client.conversations_create, kwargs =
    # {"name" : post_to_channel, "is_private": True})
    # channel_id = response["channel"]["id"]
    # response = rate_limit(logger, client.conversations_invite, kwargs =
    # {"channel" : channel_id, "users": "U01JVQYA21X"})
    # response = rate_limit(logger, say, kwargs =
    # {"channel" : channel_id, "text" : text})
    # return response


def foward_message(client, say, channel, ts, reason, post_to_channel, add_link,
                   logger):
    # Create permalink for original message ##
    permalink = rate_limit(logger, client.chat_getPermalink, kwargs={
                           "channel": channel, "message_ts": ts})['permalink']
    # Message fowarded from bot ##
    text = f'''{reason}\n The original message: <{permalink}| >'''
    if add_link:
        text = f'''{reason}\n The following link will take you to the original
message: <{permalink}|*Show original message*>'''
    # try:
    response = rate_limit(logger, say, kwargs={
                          "channel": post_to_channel, "text": text})
    # except:
    # response = create_channel(client, post_to_channel, say, text, logger)
    return response['ts'], response['channel']


def eph_message(message, client, say, text, post_to_channel, reason, logger):
    user = message['user']
    # Might be an API call we can do less by getiing the information
    # else where.
    BOT_ID = client.api_call('auth.test')['user_id']
    if BOT_ID != user:
        channel = message['channel']
        ts = message['ts']
        foward_ts, foward_channel = foward_message(
            client, say, channel, ts, reason, post_to_channel, True, logger)
        blocks = eph_message_block(text, ts, foward_ts, foward_channel)
        rate_limit(logger, client.chat_postEphemeral, kwargs={
                   "channel": channel, "blocks": blocks, "user": user,
                   "text": text})


def reply_in_thread(message, client, say, text, post_to_channel, reason,
                    foward_message, logger):
    user = message['user']
    BOT_ID = client.api_call('auth.test')['user_id']
    if BOT_ID != user:
        channel = message['channel']
        ts = message['ts']
        if foward_message:
            foward_ts, foward_channel = foward_message(
                client, say, channel, ts, reason,
                post_to_channel, True, logger)
        rate_limit(logger, client.chat_postMessage, kwargs={
                   "channel": channel, "user": user, "thread_ts": ts,
                   "text": text})

# Routes
# Listening
# Listening if any of the following words is in a send message (ignoring
# case sensitivity) password, pwd, passwd, p-word, paswd, secrete word,
# passwords


@app.message(re.compile(r'''(?:^|\W)(?<!\/|=|\+|&|-|_|\?)(password|pasword|pw|pwd|passwd|p-word|paswd
|secret word|passwords|paswords)(?!\/|=|\+|&|-|_)(?:$|\W)''', re.I))
def password_message(ack, client, message, say, logger):
    ack()
    thread_reply_message = '''I recognized that you might be talking about passwords!
:closed_lock_with_key:\n You are *not allowed* :no_entry: to share any
passwords on Slack. If that is the case, please *delete* your message
immediately.'''
    post_to_channel = 'C01TJL6DV6K'
    reason = ''':warning: :closed_lock_with_key: Potential sharing of a
password :closed_lock_with_key: :warning:'''
    reply_in_thread(message, client, say, thread_reply_message,
                    post_to_channel, reason, False, logger)


# Checking if a postal code is recognized in any send message on slack.
# If so the bot sends an ephemeral message to the user stating that he is not
# allowed no share any custumer information on slack
@app.message(re.compile(r'''(?:^|\W)(?<!\/|=|\+|&|-|_|\?)(?!CV4 8LG|CV48LG|NG1 4BX|
NG14BX|EC1M 6PB|EC1M6PB|NG1 6HD|NG16HD|NG1 9NJ|NG19NJ|LE1 1TQ|LE11TQ)([A-Z][A-H
J-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})(?!\/|=|\+|&|-|_)(?:$|\W)''', re.I))
def postcode_message(ack, payload, client, message, say, logger):
    ack()
    print('here')
    eph_mes_text = '''I recognized a UK postcode!:house_with_garden: \n You are
*not allowed * :no_entry: to share any sensitive customer data such as
names :bust_in_silhouette:, home addresses :house_with_garden:, emails
:e-mail:, credit card information :credit_card: and more...\n If that
is the case, please * delete * your message immediately. Only share the
customer ID!'''
    post_to_channel = 'C01TJL6DV6K'
    reason = ''':warning: :house_with_garden: Potential sharing of a customer
address :house_with_garden: :warning: '''
    eph_message(message, client, say, eph_mes_text,
                post_to_channel, reason, logger)


# Checking if a credit card number is recognized in any send message on slack.
# If so the bot sends an ephemeral message to the user stating that he is not
# allowed no share any customer information on slack
@app.message(re.compile(r'''(?:^|\W)(?<!\/|=|\+|&|-|_|\?)(?:4\d{3}|5[1-5]\d{2}|6011|3[47]\d{2})([-\s]?)
\d{4}\1\d{4}\1\d{3,4}(?!\/|=|\+|&|-|_)(?:$|\W)'''))
def creditcard_message(ack, client, message, say, logger):
    ack()
    eph_mes_text = '''I recognized a Credit card number! :credit_card: \n You are
*not allowed * :no_entry: to share any sensitive customer data such as:
names: bust_in_silhouette:, home addresses :house_with_garden: ,
emails :e-mail: , credit card information :credit_card: and more...\n If
that is the case, please * delete * your message immediately. Only share
the customer ID!'''
    post_to_channel = 'C01TJL6DV6K'
    reason = ''':warning: :credit_card: Potential sharing of a credit card
number:credit_card: :warning: '''
    eph_message(message, client, say, eph_mes_text,
                post_to_channel, reason, logger)


# Checking if a sort code or bank account number is recognized any send
# message on slack.
# If so the bot sends an ephemeral message to the user stating that he is not
# allowed no share any customer information on slack
@app.message(re.compile(r'''(?:^|\W)(?<!\/|=|\+|&|-|_|\?)(?!60 80 09|608009|60-80-09|70257647|
70337349|70312540|70371040|70238189|36166219|36166103|36166138|61125970|
50 00 00|500000|50-00-00|20571852|20571895|20571925|20571615|20571623|60-60-05|
60 60 05|606005|30298249|09-07-20|09 07 20|090720|06045006|01571311|20571828|
20571968|20571704|30-93-71|309371|30 93 71|00013647|30-00-02|300002|30 00 02|
00305559)(?<!A-
)([1-9]{2}\s?\-?[1-9]{2}\s?\-?[1-9]{2}|(\d){7,8})(?!\/|=|\+|&|-|_)(?:$|\W)'''))
def bank_information(ack, client, message, say, logger):
    ack()
    eph_mes_text = '''I recognized a UK sort code or Bank account number!
:bank: \n You are * not allowed *:no_entry: to share any sensitive
customer data such as: names: bust_in_silhouette:, home addresses
:house_with_garden:, emails :e-mail: , credit card information
:credit_card: and more...\n If that is the case, please * delete *
your message immediately. Only share the customer ID!'''
    post_to_channel = 'C01TJL6DV6K'
    reason = ''':warning: :credit_card: Potential sharing of a a UK sort code or
Bank account number :bank: :warning: '''
    eph_message(message, client, say, eph_mes_text,
                post_to_channel, reason, logger)

# edits


def get_message(channel, text, username, icon):
    return {
        "channel": channel,
        "username": username,
        "icon_emoji": icon,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ],
    }


def add_user_to_channel(channel, user, client):
    members_of_channel = client.conversations_members(channel=channel)
    if user not in members_of_channel['members']:
        client.conversations_invite(channel=channel, users=user)


def delete_message(original_channel, ts, logger):
    rate_limit(logger, user_client.chat_delete, kwargs={
        'channel': original_channel, 'ts': ts, 'as_user': True})


def send_direct_message(user_id, client, dm_text, username, icon, logger):
    message = get_message(user_id, dm_text, username,
                          icon)
    rate_limit(logger, client.chat_postMessage, kwargs={**message})


@app.event("reaction_added")
def admin_delete_offending_message(ack, event, client, logger):
    ack()
    channel = event['item']['channel']
    if event['reaction'] == 'x' and (channel
                                     == 'C01TJL6DV6K'):
        ts = event['item']['ts']
        response = client.conversations_history(
            channel=channel,
            inclusive=True,
            oldest=ts,
            limit=1)
        text = 'Admin deleted message :white_check_mark:'
        original_message = response['messages'][0]['attachments'][0]
        dm_text = 'Admins have removed your message: ' + \
            original_message['fallback']
        send_direct_message(
            original_message['author_id'], client, dm_text, "Admin bot", ":x:",
            logger)
        delete_message(original_message['channel_id'],
                       original_message['ts'], logger)
        rate_limit(logger, client.chat_update, kwargs={
            "channel": channel, "ts": ts, "text": text})


@app.message(re.compile(r'''(?:^|\W)(xoserve|ecoes)(?:$|\W)''', re.I))
def ecoes_search(ack, client, message, say, logger):
    ack()
    ecoes_channel = 'C020623RQRW'
    user_id = message['user']
    channel = message['channel']
    ts = message['ts']
    reason = '''This user has posted something about Ecoes or Xoserve, we have moved
his comment into this channel for security reasons and added them.'''
    eph_mes_text = '''Welcome to the ecoes/xoserve chat, please use this chat to talk
about all things ecoes/xoserve'''
    user_profile = client.users_profile_get(user=user_id)
    user_email = user_profile['profile']['email']
    if '@eonnext.com' in user_email:
        add_user_to_channel(ecoes_channel, user_id, client)
        foward_ts, foward_channel = foward_message(
            client, say, channel, ts, reason, ecoes_channel, False, logger)
        permalink = rate_limit(logger, client.chat_getPermalink, kwargs={
            "channel": foward_channel,
            "message_ts": foward_ts})['permalink']
        rate_limit(logger, client.chat_postEphemeral, kwargs={
                   "channel": ecoes_channel, "user": user_id,
                   "text": eph_mes_text})
        dm_text = f'''I see your talking about Xoserve or Ecoes. I've moved your comment
into the private channel for security reasons.
<{permalink}|*Show original message*>'''
        send_direct_message(user_id, client, dm_text,
                            "Ecoes", ":closed_lock_with_key:", logger)
        delete_message(channel, ts, logger)
    else:
        thread_reply_message = '''Hey, I noticed you were talking about ecoes/xoserve
did you know we have a private channel for all employees? I recognise you are
not registered with an E.ON Next email, if you would like to join please make a
request with one of the admins:'''
        reply_in_thread(message, client, say,
                        thread_reply_message, '', '', False, logger)

    # edits

    # Checking if a file has been attached to a send message
    # If so the bot sends an ephemeral message to the user reminding to be
    # carefull not to share any sensitive data in the files


@ app.event({
    "type": "message",
    "subtype": "file_share"
})
def file_share(ack, client, message, say, logger):
    ack()
    eph_mes_text = '''When you share a file: file_folder: please be carefull it
doesn't contain any sensitive customer information, such as: names
:bust_in_silhouette: , home addresses :house_with_garden: , emails
:e-mail: , credit card information: credit_card: and more... '''
    post_to_channel = 'C01TJL6DV6K'
    reason = 'A file has been shared :file_folder:'
    eph_message(message, client, say, eph_mes_text,
                post_to_channel, reason, logger)


@ app.event("channel_created")
def join_new_channel(ack, event, client, logger):
    ack()
    channel = event['channel']['id']
    rate_limit(logger, client.conversations_join,
               kwargs={"channel": channel})


def check_if_deleted(client, channel, ts):
    result = client.conversations_history(
        channel=channel, inclusive=True, oldest=ts, limit=1)
    if result['messages'][0]['text'] == 'Message deleted :white_check_mark:':
        return True
    return False

# Actions #


@ app.action('delete')
def delete(ack, body, client, logger):
    ack()
    two_ts_list = body['actions'][0]['value'].split(",")
    original_message_ts = two_ts_list[0]
    original_channel = body['container']['channel_id']
    rate_limit(logger, user_client.chat_delete, kwargs={
               'channel': original_channel, 'ts': original_message_ts,
               'as_user': True})
    foward_ts = two_ts_list[1]
    foward_channel = body['actions'][0]['block_id']
    text = 'The user has deleted his message :white_check_mark:'
    admin_deleted_message = check_if_deleted(client, foward_channel, foward_ts)
    if not admin_deleted_message:
        rate_limit(logger, client.chat_update, kwargs={
            "channel": foward_channel, "ts": foward_ts, "text": text})
    delete_eph_message(body, logger)


@ app.action('ignore')
def ignore(ack, client, body, logger):
    ack()
    foward_ts = body['actions'][0]['value']
    foward_channel = body['actions'][0]['block_id']
    text = ''':warning: You might want to * double check *! The user considers
    that his message does not contain any sensitve data. :warning:'''
    admin_deleted_message = check_if_deleted(client, foward_channel, foward_ts)
    if not admin_deleted_message:
        rate_limit(logger, client.chat_update, kwargs={
            "channel": foward_channel, "ts": foward_ts, "text": text})
    delete_eph_message(body, logger)
# respond to any other event


@ app.event({
    "type": "message"
})
def message_deleted(ack):
    ack()


if __name__ == "__main__":
    app.start(5000)


# OUTAGE ALERT SYSTEM

@app.command("/outage-alert")
def outage_command(ack, payload, client, logger):
    ack()
    client.views_open(
        trigger_id=payload['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "outage-alert",
            "title": {
                "type": "plain_text",
                "text": "Password for outage",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                            "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Password",
                        "emoji": True
                    }
                }
            ]
        }
    )


@app.view_submission("outage-alert")
def view_submit(ack, body, client, logger):
    ack()
    password = 'pass'
    block_key = list(body['view']['state']['values'].keys())
    value = body['view']['state']['values'][
        block_key[0]]['plain_text_input-action']['value']
    if value == password:
        client.views_open(
            trigger_id=body['trigger_id'],
            view={
                "type": "modal",
                "callback_id": "outage-alert-form",
                "submit": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": False
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": False
                },
                "title": {
                    "type": "plain_text",
                    "text": "Outage alert form",
                    "emoji": False
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": "Please pick the services *that are down.*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "actions",
                        "elements": [
                                {
                                    "type": "checkboxes",
                                    "options": [
                                            {
                                                "text": {
                                                    "type": "mrkdwn",
                                                    "text": "*service 1*"
                                                },
                                                "value": "value-0"
                                            },
                                        {
                                                "text": {
                                                    "type": "mrkdwn",
                                                    "text": "*service 2*"
                                                },
                                                "value": "value-1"
                                        },
                                        {
                                                "text": {
                                                    "type": "mrkdwn",
                                                    "text": "*service 3*"
                                                },
                                                "value": "value-2"
                                        }
                                    ]
                                }
                        ]
                    },
                    {
                        "type": "input",
                        "optional": True,
                        "element": {
                                "type": "plain_text_input",
                                "action_id": "outage_alert_notes",
                                "multiline": True,
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "E.g. Customers are being hung-up on when in the que."
                                },
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Notes",
                            "emoji": False
                        }
                    }
                ]
            }
        )
    else:
        client.views_open(
            trigger_id=body['trigger_id'],
            view={
                "type": "modal",
                "callback_id": "outage-alert",
                "title": {
                    "type": "plain_text",
                    "text": "Password for outage",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Password incorrect! Please try again.*"
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                                "type": "plain_text_input",
                            "action_id": "plain_text_input-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Password",
                            "emoji": True
                        }
                    }
                ]
            }
        )


@app.view_submission("outage-alert-form")
def outage_submitted(ack, body, client, logger):
    ack()
    # Anton to send body to his waterfall functions
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "outage-alert",
            "title": {
                "type": "plain_text",
                    "text": "Outage submitted",
                    "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Form successfully submitted! Thank you.*"
                    }
                }
            ]
        }
    )
