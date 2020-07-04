import logging

# define constants for convenient setting in the modules
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR

# create & expose formatter to other modules so we can add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')

def StreamHandler(stream=None):
    return logging.StreamHandler(stream)

def getLogger(name, filename="todos.log", log_level=DEBUG):
    log = logging.getLogger(name)
    log.setLevel(log_level)

    # create file handler which logs even debug messages
    if (filename):
        fh = logging.FileHandler("/var/log/{0}".format(filename))
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log
