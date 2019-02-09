from slack import Slack
from utils import *
import requests

class Location():
    def __init__(self, slack, uid, secret):
        self.slack = slack
        self.uid = uid
        self.secret = secret
        self.token = self.get_token()
        self.smala = ['apeyret', 'aguiot--', 'clfoltra', 'cvignal', 'gchainet', 'gdrai', 'glavigno', 'oel-ayad', 'sboulaao', 'thdervil']
        self.other = ['aguiot--', 'alagroy', 'bprunevi', 'hklein', 'jpoulvel', 'ktlili', 'morgani', 'rodaniel']
        self.id = {
                "apeyret":  '40321',
                "aguiot--": '40284',
                "alagroy":  '40298',
                "bprunevi": '40322',
                "clfoltra": '40591',
                "cvignal":  '40525',
                "gchainet": '40521',
                "gdrai":    '40597',
                "glavigno": '40132',
                "hklein":   '40096',
                "jpoulvel": '40652',
                "ktlili":   '26162',
                "morgani":  '40191',
                "oel-ayad": '40185',
                "sboulaao": '40556',
                "rodaniel": '27519',
                "thdervil": '40308'
                }

    def get_token(self):
        d = {'grant_type': 'client_credentials',
            'client_id': self.uid,
            'client_secret': self.secret}
        r = requests.post("https://api.intra.42.fr/oauth/token", data=d)
        if r.status_code != 200:
            return None
        token = r.json()['access_token']
        debug("New token (" + token + ")")
        return token

    def get_api(self, url='/users/apeyret'):
        data = requests.get("https://api.intra.42.fr/v2" + url, headers={'Authorization': 'Bearer ' + self.token})
        if data.status_code == 404:
            return None
        elif data.status_code == 401:
            self.token = self.get_token()
            return self.get_location()
        elif data.status_code == 200:
            data_json = data.json()
            return data_json
        else:
            return None

    def concat_user(self, users):
        bol = False
        cct = ''
        for user in users:
            if bol:
                cct += ','
            cct += self.id[user]
            bol = True
        return cct


    def get_location(self, users):
        data = self.get_api("/campus/1/locations?filter[active]=true&filter[user_id]=" + self.concat_user(users))
        if data == None:
            return ''
        return (data)

    def get_info(self, user, info):
        if user[:3] == 'lif':
            return 'https://www.youtube.com/watch?v=qMtQE1lbPho\n'
        data = self.get_api("/users/" + user)
        if data == None:
            return user + " n'a pas ete trouve\n"
        lct = str(data[info])
        if lct == None:
            return ''
        return user + ': `' + lct + '`\n'

    def location_all(self, user=None):
        lct = ''
        if user == 'o':
            datas = self.get_location(self.other)
        else:
            datas = self.get_location(self.smala)
        for data in datas:
            lct += data['user']['login'] + ': `' + data['host'] + '`\n'
        if lct == '':
            return "Personne n'est connecté"
        return lct

    def send_info(self, users, info):
        lct = ''
        if len(users) == 0 and info == "location":
            lct = self.location_all('other')
        else:
            for user in users:
                if user == 'other':
                    tmp = self.location_all('o')
                else:
                    tmp = self.get_info(user, info)
                if tmp != '':
                    lct += tmp;
                else:
                    lct += user + ': `Unavailable`\n'
        self.slack.postmsg(lct)
