from datetime import datetime
import logging
# logging.basicConfig(filename='/config/my.log', level=logging.INFO)

def log_info(message):
    '''print pretty timestamped logs'''
    ts = datetime.now()

    # logging.info("%s | %s" % (ts, message))
    print("%s | %s" % (ts, message))

def log_error(message):
    '''print pretty timestamped logs'''
    ts = datetime.now()

    print("%s | %s" % (ts, message))