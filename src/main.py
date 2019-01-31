import os
import time
from location   import Location
from slack      import Slack

slack_token = os.environ["SLACK_API_TOKEN"]
slack = Slack(slack_token)
lct = Location(
        slack=slack,
        uid="988bf8f381824571cfa3b4dc1e591904ccdf00549a2f86b7d96d2c380783b4bc",
        secret="27da4f23ef3e682f6a3e7f8ba3db55e572582e038ae65b349bd3f4780e9810ec")

print(lct.token)
slack.run(lct)
