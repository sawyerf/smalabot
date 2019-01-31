import os
import time
from slackclient import SlackClient
from location import Location

def router(lct, msg):
    print(msg)
    if msg[:4] == '!lct':
        lct.send_location(msg.split(" ")[1:])

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
lct = Location(
        sc=sc,
        uid="988bf8f381824571cfa3b4dc1e591904ccdf00549a2f86b7d96d2c380783b4bc",
        secret="27da4f23ef3e682f6a3e7f8ba3db55e572582e038ae65b349bd3f4780e9810ec")

print(lct.token)
if sc.rtm_connect():
  while sc.server.connected is True:
      lol = sc.rtm_read()
      for msg in lol:
          if msg['type'] == 'message':
              if msg['channel'] == 'CFTUZTEM7':
                    router(lct, msg['text'])
