import time

def debug(str):
	fd = open("/smalabot/log", "a")
	fd.write("[" + time.strftime("%d %B %H:%M:%S") + "] " + str + "\n")
	fd.close()
