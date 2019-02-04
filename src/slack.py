from slackclient    import SlackClient

class   Slack():
    def __init__(self, token):
        self.sc = SlackClient(token)

    def postmsg(self, msg, channel="CFTUZTEM7"):
        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=msg
        )

    def router(self, msg, lct):
        print(msg)
        if msg[:4] == '!lct':
            lct.send_location(msg.split(" ")[1:])
        elif msg[:5] == '!ping':
            self.postmsg("pong")
        elif msg[:5] == '!help':
            self.postmsg("""help:
```!help  affiche ce message
!lct   affiche les place de la smala```""")

    def run(self, lct):
        if self.sc.rtm_connect():
            self.postmsg("Smalabot est connecté")
            while self.sc.server.connected is True:
                msgs = self.sc.rtm_read()
                for msg in msgs:
                    print(msg)
                    if msg['type'] == 'message' and msg['channel'] == 'CFTUZTEM7':
                            self.router(msg['text'], lct)
