# coding: utf-8
from selenium import webdriver
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
# driver = webdriver.Firefox(profile)
# # driver.implicitly_wait(10) # seconds

AM = 'A'
PM = 'P'

# generate a random temperature based on APM
def generate_temp(apm):
    base_part = 36.0 if apm == AM else 36.5
    rand_part = random.random() * 0.5
    temp = base_part + rand_part
    temp = round(temp, 1)
    return str(temp)


# upload the temperature
def upload_temp(apm = PM):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    # read the config from JSON file
    with open('config', 'r') as f:
        config = json.load(f)
    url = config['url']
    user = config['user']
    psw = config['password']

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # login to the web site
    ele_user = driver.find_element_by_id('userNameInput')
    ele_user.send_keys(user)
    ele_psw = driver.find_element_by_id('passwordInput')
    ele_psw.send_keys(psw)
    ele_psw.send_keys(Keys.ENTER)

    # no for symptoms flag
    radio_symptom = wait.until(EC.element_to_be_clickable((By.NAME, 'symptomsFlag')))
    radio_symptom.click()

    # no for family symptoms flag
    radio_family_symptom = wait.until(EC.element_to_be_clickable((By.NAME, 'familySymptomsFlag')))
    radio_family_symptom.click()

    # set temperature
    input_temp = wait.until(EC.presence_of_element_located((By.ID, 'temperature')))
    temp = generate_temp(apm)
    input_temp.send_keys(temp)

    # set AM or PM
    driver.execute_script("document.dlytemperature.declFrequency.value = " + "'" + apm + "'" + ";")

    # disable the web driver detector
    driver.execute_script("document.dlytemperature.webdriverFlag.value = '';")

    btn_submit = wait.until(EC.element_to_be_clickable((By.NAME, 'Save')))
    btn_submit.click()
    driver.close()

upload_temp(AM)