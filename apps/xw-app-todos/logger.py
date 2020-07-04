import logging

# --- constants
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
LOG_FILENAME = "todos.log"
LOG_FULLNAME = "/var/log/{0}".format(LOG_FILENAME)

# ---
formatter = logging.Formatter('%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')

def StreamHandler(stream=None):
    return logging.StreamHandler(stream)

def getLogger(name, filename=LOG_FILENAME, log_level=DEBUG):
    log = logging.getLogger(name)
    log.setLevel(log_level)
    if (filename):
        fh = logging.FileHandler(LOG_FULLNAME)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
