from    slack import Slack
import requests

class Location():
    def __init__(self, slack, uid, secret):
        self.slack = slack
        self.uid = uid
        self.secret = secret
        self.token = self.get_token()
        self.smala = ['apeyret', 'clfoltra', 'cvignal', 'gchainet', 'gdrai', 'glavigno', 'oel-ayad', 'sboulaao', 'thdervil']

    def get_token(self):
        d = {'grant_type': 'client_credentials',
            'client_id': self.uid,
            'client_secret': self.secret}
        r = requests.post("https://api.intra.42.fr/oauth/token", data=d)
        return r.json()['access_token']

    def get_location(self):
        data = requests.get("https://api.intra.42.fr/v2/campus/1/locations", headers={'Authorization': 'Bearer ' + self.token})
        if data.status_code == 404:
            return user + " not found\n"
        elif data.status_code == 401:
            self.token = self.get_token()
            return self.get_location()
        data_json = data.json()
        return data_json

    def location_search(self, places, user):
        for place in places:
            if place['user']['login'] == user:
                return user + ': `' + place['host'] + '`\n'
        return ''

    def location_all(self):
        lct = ''
        places = self.get_location()
        for user in self.smala:
            lct += self.location_search(places, user)
        if lct == '':
            return "Personne n'est connecté"
        return lct

    def location_of(self, users):
        lct = ''
        places = self.get_location()
        for user in users:
            tmp = self.location_search(places, user)
            if tmp == '':
                lct += user + ':  `Unavailable`\n'
            else:
                lct += tmp
        return lct

    def send_location(self, users):
        lct = ''
        if len(users) == 0:
            lct = self.location_all()
        else:
            lct = self.location_of(users)
        self.slack.postmsg(lct)
