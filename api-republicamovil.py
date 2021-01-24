import os
import json
from sys import platform
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
if(soup.select_one('.percent')):
    promo_available = True
    promo = soup.select_one('.percent')
else:
    promo_available = False

for idx, tag in enumerate(divs):
    x = ''
    char = ''
    if(idx == 0):
        char = 'minutes'
        x = tag.text.strip().split(" min")
    if(idx == 1):
        char = 'cellular'
        x = tag.text.strip().split("B")
        x[0] = x[0].partition(' ')[0]  # divide string by first space
        x[1] = x[1].partition(' ')[0]
    x = list(filter(None, x))  # remove empty items
    # print(list(filter(None, x)))
    data[char] = x

if(promo_available):
    data['promo'] = promo.text.strip().split(' / ')

f = open(DATA_FILE_PATH, 'r+')
f.truncate(0)  # emptying file
f.write('{')
f.write('\n"min_used": "' + data['minutes'][0] + '",')
f.write('\n"min_available": "' + data['minutes'][1] + '",')
f.write('\n"cel_used": "' + data['cellular'][0] + '",')
f.write('\n"cel_available": "' + data['cellular'][1] + '",')
if(promo_available):
    f.write('\n"promo_used": "' + data['promo'][0].partition(' ')[0] + '",')
    f.write('\n"promo_available": "' +
            data['promo'][1].partition(' ')[0] + '"')
f.write('\n}')
f.close()

print(json.dumps(data))

# print(json.dumps(str(divs)))
