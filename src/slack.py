from slackclient    import SlackClient
from utils import *

class   Slack():
	def __init__(self, token):
		self.sc = SlackClient(token)
		if self.sc.rtm_connect():
			self.start = True
		else:
			self.start = False

	def postmsg(self, msg, channel="CFTUZTEM7"):
		self.sc.api_call(
			"chat.postMessage",
			channel=channel,
			text=msg
		)

	def get_msg(self):
		lst = []
		if  self.start and self.sc.server.connected is True:
			msgs = self.sc.rtm_read()
			for msg in msgs:
				if msg['type'] == 'message' and msg['channel'] == 'CFTUZTEM7' \
					and 'text' in msg and not 'bot_id' in msg:
					lst.append(msg['text'])
			return lst
		else:
			return None
