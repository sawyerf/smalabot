import os
import time
from slackclient import SlackClient
import requests

def get_token():
    uid = "988bf8f381824571cfa3b4dc1e591904ccdf00549a2f86b7d96d2c380783b4bc"
    secret = "27da4f23ef3e682f6a3e7f8ba3db55e572582e038ae65b349bd3f4780e9810ec"
    d = {'grant_type': 'client_credentials',
        'client_id': uid,
        'client_secret': secret}
    r = requests.post("https://api.intra.42.fr/oauth/token", data=d)
    return r.json()['access_token']

def location_of(token, user):
    lol = requests.get("https://api.intra.42.fr/v2/users/" + user, headers={'Authorization': 'Bearer ' + token})
    dat = lol.json()['location']
    if dat == None:
        return ''
    return user + ': `' + dat + '`\n'

def location_all(token):
    smala = ['apeyret', 'oel-ayad', 'cvignal', 'clfoltra', 'glavigno', 'sboulaao', 'thdervil', 'gchainet']
    lct = ''
    for user in smala:
        lct += location_of(token, user)
    return lct

def send_location(token, users):
    lct = ''
    if len(users) == 0:
        lct = location_all(token)
    else:
        for user in users:
            tmp = location_of(token, user)
            if tmp != '':
                lct += tmp;
            else:
                lct += user + ': `Unavailable`\n'
    sc.api_call(
        "chat.postMessage",
        channel="CFTUZTEM7",
        text=lct)

def router(msg, token):
    if msg[:4] == '!lct':
        send_location(token, msg.split(" ")[1:])

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
token = get_token()
if sc.rtm_connect():
  while sc.server.connected is True:
      lol = sc.rtm_read()
      for msg in lol:
          if msg['type'] == 'message':
              if msg['channel'] == 'CFTUZTEM7':
                    router(msg['text'], token)
