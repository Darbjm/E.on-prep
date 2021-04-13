from slack import WebClient

# from slack.errors import SlackApiError
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path(".") / "env"
load_dotenv(dotenv_path=env_path)

client = WebClient(token=os.environ["SLACK_TOKEN"])
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events", app
)
# try:
#     client.conversations_join(channel="C01TSMCHJDU")
#     response = client.chat_postMessage(channel="#testing",
# text="Hello world!")
#     assert response["message"]["text"] == "Hello world!"
# except SlackApiError as e:
#     assert e.response["ok"] is False
#     assert e.response["error"]
#     print(f"Got an error: {e.response['error']}")


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    # user_id = event.get("user")
    text = event.get("text")

    client.chat_postMessage(channel=channel_id, text=text)


if __name__ == "__main__":
    app.run(debug=True)
