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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B8BA1DA9A5C608179FA5023FA7F9E17A2741E18817C034E12417F9D13BD8E53458B2FB0A1506B67738B0E3080F46E0C6B2C4FB36CD8EAF44E92EB5122463F33702BA4980D451BE8F78DC852C843C29670F95E16C5FBE33615747E7C648775F20D8B48E5BA10956E8D68B7893D403C4C39CF07E516C1A99AE33EB7C6B3BF2542AAB76D4FF9E018D39636AF94F44C798D74622E305E0993D855079A68CD3C0F482F71026C41A4D008EF70E3DAC5D256460F9231BC46DB6F128E0654F57553C318E0476ED509F6CB15999EF5E6C1EC868160E2508AE9DB888E19AED3C7C4C25E0C09F3E7EF54CC83070FB219F155CB55748484977FA37EE05DFEB201F7607E3C9741FB3F7B1B8942BD2C78F89DCDFBCAD5E4003EBAD57517B815CDDCC1286D258B46D8FB39C34B72B4CBA1611BDFEC2EBDC264C7CF3283A6DAECD09E4CD9FB9255D2B8ED22A3CEE48267A82F2E546CBA0D82D5FEC6CDCDA0EB761A0F4B5B3872F5D"})
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
