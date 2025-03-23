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
    browser.add_cookie({"name": "MUSIC_U", "value": "007A4DD2DEBAF1CFAE8B7AB65E3AFB11154E5DCAE755E18A51958C32BEFFE1A87A64BDDADFFE44AFACAA29C6D2AD00FF00FBDBB9DE2AB80ABC3034FF2199088A3E3F0748C8B5940AED0384524259554DBE5EDF971704125237A3096B1A2C9D473016982450999FD99BD410C43EB37B978259C8BAB56425B6B2ECE57B679ADD829D9A76BBD4853983B1558D7879DD6D67B2FC7637099D0638B2294D620CC474D4383766AD532E1471B3C6794BD49B4D832DE5DD1604484403C69BBC679EBDE9B043AA98112FF8BE2EF694FC5CEF49E843C6D164C9A56AC5F51DD15177E1BD772086DBD7CDD6782E6DAC8BAC8BD340E5A009F82336028B6F7A253FBF92B47C544B2F3E42DCC018A3B87C85E4264A29DDC81F687635AB7B61FC898A4CF8BACEAA49C10BD7DFF20234C1F7A6AD2359472CCCA5024EC0B35035E04BA51CD66E691893E3387EF63459B5C62FF2952333FABB1F5D040900B65F71F02A4FACFA979CD49365"})
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
