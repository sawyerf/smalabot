import os
import time
from location   import Location
from slack      import Slack
from router     import Router
from utils      import debug


slack_token = os.environ["SLACK_API_TOKEN"]
ft_uid = os.environ["ft_uid"]
ft_secret = os.environ["ft_secret"]

slack = Slack(slack_token)
lct = Location(
        slack=slack,
        uid=ft_uid,
        secret=ft_secret)
rout = Router(slack, lct)

slack.postmsg("Smalabot est connecté")
while True:
    msgs = slack.get_msg()
    if msgs == None:
        debug("Message Slack vide")
        continue
    for msg in msgs:
        rout.router(msg)
