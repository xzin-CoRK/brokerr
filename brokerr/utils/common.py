from datetime import datetime
import logging
import os
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

def create_base_screenshot_directory():
    # Create the base directory for screenshots
    screenshots_directory = '/config/screenshots'

    if not os.path.exists(screenshots_directory):
        try:
            os.makedirs(screenshots_directory)
            print(f"Directory '{screenshots_directory}' created.")
        except OSError as e:
            print(f"Error creating directory '{screenshots_directory}': {e}")