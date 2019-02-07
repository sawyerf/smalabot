import os
import time
from location   import Location
from slack      import Slack

slack_token = os.environ["SLACK_API_TOKEN"]
ft_uid = os.environ["ft_uid"]
ft_secret = os.environ["ft_secret"]

slack = Slack(slack_token)
lct = Location(
        slack=slack,
        uid=ft_uid,
        secret=ft_secret)

slack.run(lct)
