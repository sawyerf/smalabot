from utils  import debug
class Router():
	def __init__(self, slack, lct):
		self.slack = slack
		self.lct = lct
		self.help = self.get_help()

	def get_help(self):
		fd = open("/smalabot/src/help", 'r')
		ret = fd.read()
		fd.close()
		return ret

	def router(self, msg):
		debug(msg)
		msgs = msg.split(" ")
		if msgs[0] == '!lct':
			self.lct.send_info(msgs[1:], "location")
		elif msgs[0] == "!phone":
			self.lct.send_info(msgs[1:], "phone")
		elif msgs[0] == "!id":
			self.lct.send_info(msgs[1:], "id")
		elif msgs[0] == "!bite":
			self.lct.get_free_place()
		elif msgs[0] == "!free":
			self.lct.get_free_place()
		elif msgs[0] == '!ping':
			self.slack.postmsg("pong")
		elif msgs[0] == '!help':
			self.slack.postmsg(self.help)
		else:
			self.slack.postmsg(":shushing_face:")

