from slack import WebClient
from slack.errors import SlackApiError
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.')/'env'
load_dotenv(dotenv_path=env_path)

client = WebClient(token=os.environ['SLACK_TOKEN'])

try:
    client.conversations_join(channel="C01U5JCV6EQ")
    response = client.chat_postMessage(
        channel='#general',
        text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")
