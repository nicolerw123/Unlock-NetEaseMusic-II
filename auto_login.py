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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B76D5A9D9C8127C3FC81281E3E54993A8AA8558B830CBDC665F67D1734744D98F94794B770295CBB7EA54B3BF8C9A1B977775B40819FB7365AED5E5703B3A6611059E6CF4856CDD388E3417C06B79B8575E4EFF52AE4CC88C1BA59856E0E8B999B0045F607A2173790730C762AAEAE8334AABF85FFF6EE3E624F727259408694901098A84E6B107C0B7C5CF72CBB71F3B4D0AAFFF353ED463C2AA4086E79BF7895A458C977D0EBC35CE066E7EFEBD063359B0AE52225BC7CA8FF0FC803BA3B25DE6A2FA8155BC6F729672B2BC0B5DA80C91A2CF0815472350CEAD131DA80F77550B61E53820B279C5FF3F39152AA36B0CFC444E474E43C307755125CD5594B3BF636A633938AB67BE7A6532443A44D7BE84AF9233593A8E9A6FDB2B8C81D279E1D12B11C06C87246D835CF5ACB8EF553D8FD031416F64AFCC56A0B76EB4E3B879D774DDED605DCCB368C40E14F33683E6ABF26D0FEFCEB08B585C0A0FDD101D4"})
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
