import logging

# --- constants
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
LOG_FILENAME = "reports.log"
LOG_FULLNAME = "/var/log/{0}".format(LOG_FILENAME)

# ---
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s - %(message)s')

def getLogger(name, filename=LOG_FILENAME, log_level=DEBUG):
    log = logging.getLogger(name)
    log.propagate = False
    log.setLevel(log_level)
    if (filename):
        fileHandler = logging.FileHandler(LOG_FULLNAME)
        fileHandler.setLevel(log_level)
        fileHandler.setFormatter(formatter)
        log.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(log_level)
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    
    return log
