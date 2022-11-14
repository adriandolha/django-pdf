import base64
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from django_pdf.logger import LOGGER

appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }
    ],
    'landscape': False,
    'paperWidth': 8.27,
    'paperHeight': 11.69,
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False
    # "mediaSize": {
    #     "height_microns": 210000,
    #     "name": "ISO_A5",
    #     "width_microns": 148000,
    #     "custom_display_name": "A5"
    # },
    # "customMargins": {},
    # "marginsType": 2,
    # "scaling": 175,
    # "scalingType": 3,
    # "scalingTypePdf": 3,
    # "isCssBackgroundEnabled": True
}

profile = {
    'printing.print_preview_sticky_settings.appState': json.dumps(appState)
}


def get_pdf():
    URL = 'http://localhost:8000/'
    driver = get_driver()

    LOGGER.debug('Starting web browser...')
    # driver.implicitly_wait(10)
    _wait = WebDriverWait(driver, 10)
    LOGGER.debug(f'Get {URL}...')
    driver.get(URL)
    LOGGER.info(f'Wait for login page to load...')

    login(_wait, driver)
    _wait.until(EC.presence_of_element_located((By.ID, 'chart_expenses_per_month')))
    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", appState)
    time.sleep(5)
    pdf_data = base64.b64decode(pdf_data['data'])
    LOGGER.info('Saved to pdf...')
    return pdf_data


def login(_wait, driver):
    _wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    username = driver.find_element(By.NAME, 'username')
    username.send_keys('admin')
    _wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    password = driver.find_element(By.NAME, 'password')
    password.send_keys('Goanga-111')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver
