# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00CEDE21FB33B62D2001E81E959433DE7737DA1A98C8B71748FB5C523D76968C3833851D5C90E0552E6ADD98528B51DFE0E6A8108FEA01EB69CE34823C11820D365CFDF8E630F1C92A6A5EB73916C269B5D98255E8B4D7C3A45365DFCC55601FCCD3192C95B8C8C4DE420EB836B0236A43287D08DD2E8BA601E89D9514E4DB7C9CA6B648F723D295C869C15E406365D6DD43A30886553E561647920BF4BCEE8B6AB2C07773C4356AD84788939CE048930A30641B0176CD2E3A6D0608E17C57350195F3E16121DBDD644263A438396B635CABD3CA1FBA4BBCAC455752E3B804BE7F0C8EB2DC2B626A9637AA10CF62AC5AC204ABF27166ECE7812FD0A683FF4C4DCB51F3BF7903692E25C8BFD3FD5C1BE8AD4B8FEE97E08122FF8D79043548B8300C6D464FEE5F6FBD50EB2E1DE6B63C6FD5C42403F3A28025E82ECACC1BC24A8C81D8225FDF4C1A0A5D44AA1F01B2A91503E83F7C022215BC95E8C868A3C404CA51"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
