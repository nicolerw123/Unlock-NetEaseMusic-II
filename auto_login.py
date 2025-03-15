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
    browser.add_cookie({"name": "MUSIC_U", "value": "0070D349762C8DEB6A71CEC34F3C7B767FA09C40637C9CD535AE836677D6F61893499A21945E152E4ECF33B12A21FE358291BD80FE807058784FD8CA5D2A7B564A5BFDF96518E3F9433668E011D7AA065C323742AAC164CEC5ABA9B7B08C35AA84F42464D2C9FBC6891229A551D251CA7E3A6CB95BAB73D2C005A856AF8E1C733B38285CE3D18375FBB67FD75376C84531943A5D4E321C1CF495EC472FA74090DEFE9B2FDA080CD589E1BAC1927B2445C72281FCA14BD3C6E64ABB3C59662492B4AE6FE8E893730628062B79AD8EA12B1601191EC6F455C94ED8FA5FF5D0FBC496F2BA9B59F0B3BC027BB697EDE93C9287FD0C630C1793232CF0A36EDE5D4689668561098CC2F3A62CA95CFFAFE72F4299EB48442F48D1FE91B20DB4D981C9EF05FC7BDC612849FA0895D83E9B78309B2284264D61F45D3DF8EDE86EAD02703CFC5351C8932670B5EC6F95AE4B235870A59876AB0F0F5855665CE39349BB3A4989"})
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
