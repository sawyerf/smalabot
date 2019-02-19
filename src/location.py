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

        self.host = [ "e2r8p1", "e2r8p2", "e2r8p3", "e2r8p4", "e2r8p5", "e2r8p6", "e2r9p1", "e2r9p2", "e2r9p3", "e2r9p4", "e2r9p5", "e2r9p6", "e2r10p1", "e2r10p2", "e2r10p3", "e2r10p4", "e2r10p5", "e2r10p6", "e2r10p7", "e2r12p1", "e2r12p2", "e2r12p3", "e2r12p4", "e2r12p5", "e2r12p6", "e2r12p7", "e2r8p8", "e2r8p10", "e2r8p12", "e2r8p14", "e2r8p7", "e2r8p9", "e2r8p11", "e2r8p13", "e2r9p8", "e2r9p10", "e2r9p12", "e2r9p7", "e2r9p9", "e2r9p11", "e2r9p13", "e2r10p8", "e2r10p10", "e2r10p12", "e2r10p14", "e2r10p16", "e2r10p9", "e2r10p11", "e2r10p13", "e2r10p15", "e2r11p8", "e2r11p10", "e2r11p12", "e2r11p14", "e2r11p16", "e2r11p9", "e2r11p11", "e2r11p13", "e2r11p15", "e2r12p8", "e2r12p10", "e2r12p12", "e2r12p14", "e2r12p16", "e2r12p9", "e2r12p11", "e2r12p13", "e2r12p15", "e2r8p15", "e2r8p17", "e2r8p19", "e2r8p21", "e2r8p16", "e2r8p18", "e2r8p20", "e2r9p14", "e2r9p16", "e2r9p18", "e2r9p20", "e2r9p15", "e2r9p17", "e2r9p19", "e2r10p17", "e2r10p19", "e2r10p21", "e2r10p23", "e2r10p18", "e2r10p20", "e2r10p22", "e2r11p17", "e2r11p19", "e2r11p21", "e2r11p23", "e2r11p18", "e2r11p20", "e2r11p22", "e2r12p17", "e2r12p19", "e2r12p21", "e2r12p23", "e2r12p18", "e2r12p20", "e2r12p22"]

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

    def get_free_place(self):
        msg = ''
        tmp = ''
        bite = False
        lst = []
        for i in range(99):
            if bite:
                tmp += ','
            tmp += self.host[i]
            bite = True
        data = self.get_api("/campus/1/locations?filter[host]={}&filter[active]=true&page[size]=100&sort=host".format(tmp))
        if data == None:
            return
        print(len(self.host))
        for i in data:
            lst.append(i['host'])
        print(lst)
        for i in self.host:
            if i in lst:
                continue
            else:
                msg += i + ', '
        self.slack.postmsg(msg)

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
