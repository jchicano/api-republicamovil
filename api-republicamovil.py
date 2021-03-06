import os
import json
import time
import random
from sys import platform
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()

USERNAME = os.getenv('RM_USERNAME')
PASSWORD = os.getenv('RM_PASSWORD')
DATA_FILE_PATH = os.getenv('API_STORAGE_FILE')

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')  # linux only
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
# options.headless = True  # also works

driver = webdriver.Chrome(
    '/usr/lib/chromium-browser/chromedriver', options=options)  # rpi
# driver = webdriver.Chrome(
#     executable_path='./webdriver/chromedriver-mac', options=options)

while True:

    driver.get('https://areaprivada.republicamovil.es/login')

    driver.implicitly_wait(10)  # up to 10 seconds to find elements

    driver.find_element_by_id('user-id').send_keys(USERNAME)
    driver.find_element_by_id('user-pass').send_keys(PASSWORD)
    driver.find_element_by_xpath(
        '//*[@id="app"]/article/div[1]/div/div/div/section/section/div/div[2]/div/form/div[4]/div/button').click()

    consumption = driver.find_element_by_xpath(
        '//*[@id="app"]/article/div[1]/div/div/div/section/section/div/div[1]/div[1]/div/article/div/div/div').get_attribute('innerHTML')

    driver.quit()
    data = {}
    soup = BeautifulSoup(consumption, 'lxml')
    divs = soup.findAll('div', {'class': 'progress-content'})
    promo_available = False
    if(soup.select_one('.percent')):
        promo_available = True
        promo = soup.select_one('.percent')

    for idx, tag in enumerate(divs):
        x = ''
        char = ''
        if(idx == 0):
            char = 'minutes'
            x = tag.text.strip().split(' min')
        if(idx == 1):
            char = 'cellular'
            x = tag.text.strip().split('B')
            if('M' in tag.text.strip().split('B')[0]):
                data['cel_used_format'] = 'MB'
            else:
                data['cel_used_format'] = 'GB'
        x[0] = x[0].partition(' ')[0]  # divide string by first space
        x[1] = x[1].partition(' ')[0]
        x = list(filter(None, x))  # remove empty items
        # print(list(filter(None, x)))
        data[char] = x

    if(promo_available):
        data['promo'] = promo.text.strip().split(' / ')
        if('M' in data['promo'][0]):
            data['promo_used_format'] = 'MB'
        else:
            data['promo_used_format'] = 'GB'

    f = open(DATA_FILE_PATH, 'r+')
    f.truncate(0)  # emptying file
    f.write('{')
    f.write('\n\t"min_used": "' + data['minutes'][0] + '",')
    f.write('\n\t"min_available": "' + data['minutes'][1] + '",')
    f.write('\n\t"cel_used": "' + data['cellular'][0] + '",')
    f.write('\n\t"cel_available": "' + data['cellular'][1] + '",')
    f.write('\n\t"cel_used_format": "' + data['cel_used_format'] + '",')
    if(promo_available):
        f.write('\n\t"promo_used": "' +
                data['promo'][0].partition(' ')[0] + '",')
        f.write('\n\t"promo_available": "' +
                data['promo'][1].partition(' ')[0] + '",')
        f.write('\n\t"promo_used_format": "' +
                data['promo_used_format'] + '",')
    f.write('\n\t"last_request": "' +
            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '"')
    f.write('\n}')
    f.close()

    print(json.dumps(data))

    # wait between 15 and 30 minutes
    t = random.randint(900, 1800)
    print('**Waiting', t, 'Seconds**')
    time.sleep(t)


# print(json.dumps(str(divs)))
