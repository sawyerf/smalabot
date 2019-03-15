from utils  import debug
from random	import randint

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

	def inspecteur(self):
		i = randint(0, 11)
		if i == 0:
			return 'Inspecteur Billy Janson à votre service'
		elif i == 1:
			return '- Comment se nomme cette ravisante demoiselle au jolie boucle brune ?\n- :blush: Alae'
		elif i == 2:
			return '"Encore une affaire pleine de rebondissement..." - Inspecteur Billy Janson'
		elif i == 3:
			return '- Encore un Segfault irresolvable...\n- Inspecteur Billy Janson a votre service'
		elif i == 4:
			return 'A qui appartient ce ternaire imbriqué ?'
		elif i == 5:
			return '"Encore un victime de vscode..." - Inspecteur Billy Janson'
		elif i == 6:
			return 'Bernadette ou est le dossier main.c ?'
		elif i == 7:
			return 'Jacques recherchez moi ce code sur tout les github à moins de 50km'
		elif i == 8:
			return 'Bernadette rentrez chez vous, l\'affaire des tigeurs à été résolu'
		elif i == 9:
			return 'Jacques lancez un avis de recherche, un petit garcon du nom de Theo n\'a pas été vu depuis belle lurette !'
		elif i == 10:
			return 'Encore un affaire de resolu!\ntututu tutu tututu tutututu...'
		elif i == 11:
			return 'Salut Bernadette ;)'
		return 'Inspecteur Billy Janson a votre service'

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
		elif msgs[0] == '!inspecteur':
			self.slack.postmsg(self.inspecteur())
		elif msgs[0][0] != '!':
			self.slack.postmsg(":shushing_face:")

