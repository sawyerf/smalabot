import time

def debug(str):
    fd = open("../log", "a")
    fd.write("[" + time.strftime("%d %B %H:%M:%S") + "] " + str + "\n")
    fd.close()
