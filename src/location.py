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

    def location_of(self, user):
        data = requests.get("https://api.intra.42.fr/v2/users/" + user, headers={'Authorization': 'Bearer ' + self.token})
        if data.status_code == 404:
            return user + " not found\n"
        elif data.status_code == 401:
            self.token = self.get_token()
            return self.location_of(user)
        lct = data.json()['location']
        if lct == None:
            return ''
        return user + ': `' + lct + '`\n'

    def location_all(self):
        lct = ''
        for user in self.smala:
            lct += self.location_of(user)
        if lct == '':
            return "Personne n'est connecté"
        return lct

    def send_location(self, users):
        lct = ''
        if len(users) == 0:
            lct = self.location_all()
        else:
            for user in users:
                tmp = self.location_of(user)
                if tmp != '':
                    lct += tmp;
                else:
                    lct += user + ': `Unavailable`\n'
        self.slack.postmsg(lct)
