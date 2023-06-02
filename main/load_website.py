"""load the website"""
import os
import sys
import time
import logging
import requests
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


def load_website(url, username, password, headless=True):
    """load the website"""
    # set up logging
    logging.basicConfig(
        filename='load_website.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # set up chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # set up driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # login
    try:
        username_field = driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys(username)
        password_field = driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
    except NoSuchElementException:
        logging.error("login failed")
        driver.quit()
        sys.exit(1)
    # wait for page to load
    try:
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_id("nav")
        )
    except NoSuchElementException:
        logging.error("login failed")
        driver.quit()
        sys.exit(1)
    # get the page source
    page_source = driver.page_source
    # quit the driver
    driver.quit()
    # return the page source
    return page_source

def _main():
    """main function"""
    # get the url from the environment
    url = os.environ.get("URL")
    # get the username from the environment
    username = os.environ.get("USERNAME")
    # get the password from the environment
    password = os.environ.get("PASSWORD")
    # load the website
    page_source = load_website(url, username, password)
    # print the page source
    print(page_source)