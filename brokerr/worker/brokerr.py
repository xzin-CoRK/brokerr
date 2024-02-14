import yaml
import os
from datetime import datetime
import time
from contextlib import closing
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import sys
sys.path.append('/brokerr')
from common import common
from common import dataLayer
from common import yamlLayer

class brokerrWorker():
    def __init__(self) -> None:
        self.config = None
        self.driver = None
    
    def __enter__(self):

        # get the config information
        self.config = yamlLayer.get_config()
        
        # set up the webdriver
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--headless')

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3)'\
                'AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79'\
                'Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'\
                ',*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
        opts.add_argument("--headers=" + str(headers))

        self.driver = webdriver.Firefox(options = opts)

        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
    
    def captureScreenshots(self, tracker_name) -> dict:

        success_count = 0
        error_count = 0
        
        # Ensure screenshot directory exists
        setup_screenshot_directory(tracker_name)

        tracker_to_capture = None

        for tracker in self.config['trackers']:
            if tracker_name in tracker:
                tracker_to_capture = tracker

        #TODO: VALIDATION; ensure tracker is valid
        
        # try:
        self.driver.get(tracker_to_capture['login_url'])
        wait = WebDriverWait(self.driver, 3)

        # enter username
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        username_input.send_keys(tracker_to_capture['username'])

        # Tick the 'Remember Me' checkbox
        remember_me = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
        remember_me.click()

        # enter password and submit
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password_input.send_keys(tracker_to_capture['password'])

        login = get_login_button(self.driver)
        if login is not None:
            login.click()
        else:
            common.log_error(f"ERROR: Cannot find the login button. Please share the following HTML on GitHub so that support can be added:\n{self.drive.page_source}")

        tracker_name = next(iter(tracker_to_capture))

        for url in tracker_to_capture['urls_to_screenshot']:
            # try:

            wait = WebDriverWait(self.driver, 2)
            common.log_info(f"Just did login. Here's what the page looks like:\n{self.driver.page_source}")

            common.log_info(f"Taking screenshot of url: {url}")

            # Load the page
            self.driver.get(url)

            # Wait for the content to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            timestamp = int(time.time())
            image_path = f"/config/screenshots/{tracker_name}/{timestamp}.png"
            self.driver.get_full_page_screenshot_as_file(image_path)

            # Store info about our successful capture in the db
            dataLayer.store_success(tracker_name, timestamp, image_path)

            success_count += 1
        
        response = {
            "success": True,
            "message": f"Finished capturing screenshots for tracker {tracker_name}. {success_count} screenshot(s) captured successfully, {error_count} error(s).",
            "success_count": success_count,
            "error_count": error_count
        }

        return response

def get_login_button(driver) -> (WebElement | None):
    """"
    Iterates through known XPATH routes to find the tracker's login button

    :param driver: the webdriver
    :return: WebElement of the login button, or None if not found
    """
    xpath_list = [
        "//input[@name='login']",                       # Gazelle-based trackers
        "//button[@class='auth-form__primary-button']"  # UNIT3D-based trackers
    ]

    for xpath in xpath_list:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return element
        except NoSuchElementException:
            pass
    
    return None

def setup_screenshot_directory(tracker = '') -> None:
    """
    Sets up the screenshots directory if it doesn't exist. Also creates a subdirectory for the specified tracker

    :param tracker: subdirectory to create
    """
    screenshots_directory = '/config/screenshots'

    if tracker:
        screenshots_directory += f'/{tracker}'

    if not os.path.exists(screenshots_directory):
        try:
            os.makedirs(screenshots_directory)
            common.log_info(f"Directory '{screenshots_directory}' created.")
        except OSError as e:
            common.log_error(f"ERROR: Error creating directory '{screenshots_directory}': {e}")