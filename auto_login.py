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
    browser.add_cookie({"name": "MUSIC_U", "value": "00071CC83DD9A3056F694164C65EFD7110D16D90099EADEED3F40B9A507696907E5B039F61B7AF27B8804CCDEB9FC5BC300CAEFD071CD41E274DD35F664AEB2855BC8CD14D37241B5BCC77267743941E8FCB8D46B42CF022FEC2F59D94DB52213193E2E15008C58BB6CF579DE8B6F42F6C8A3D40754999B3DBD0C7D2FFF5EC3638402FD7E808E3B2C7D8C752DC8E78E8AD0EC89BF35ED8F3FC54B758BC7C6B00399D056496212F7DC9EE86ADBF20B9B00CA4EFA0EDC110489CABCD76AD79700B8BE267B125FA1B151F8D73A2F9E9C734F72668711EEDCA998B1FD7C993369E058E827E9E90CE08A80EF12C5373B247086101BDE0D66F00799BD28074461E7F10BDCA96970458AECA8B04489CD48D952C04F74E9D0C111C464CB52417C4BDCA0EC4BC7B957E12D27B66DED65C1F98A8FDBC8396D3E36D91CD76A781A0CDFF6D2D71495826096C89F21B7BDBA8970D6643AE86DEFE8FCE21F3A04A04CEEA5EEA83F1"})
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
