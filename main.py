import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

print(sc.api_call(
  "chat.postMessage",
  channel="CFTUZTEM7",
  text="Hello from Python! :tada:",
))
print("lol\n")
