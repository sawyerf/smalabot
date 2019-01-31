import os
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

def location_of(user, token):
    lol = requests.get("https://api.intra.42.fr/v2/users/apeyret", headers={'Authorization': 'Bearer ' + token})
    dat = lol.json()['location']

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)


token = get_token()
print(sc.api_call(
  "chat.postMessage",
  channel="CCEELHRR6",
  text="""apeyret: {}
  oel-ayad: {}
  glavigno: {}
  cvignal: {}
  thdervil: {}""".format(location_of("apeyret", token), location_of("oel-ayad", token), location_of("glavigno", token), location_of("cvignal", token), location_of("thdervil", token)),
))
print("lol\n")
