import os
import time
import winsound
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pathlib

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random

# Setting the chrome_options
global chrome_options
chrome_options = Options()
scriptDirectory = pathlib.Path().absolute()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.add_argument('--profile-directory=Profile 8')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('disable-infobars')
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("user-data-dir=chrome-data")
chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")

# Enter NFT buying price below
buying_price = 2.1

# You need to put your NFT link here
NFT_link = "https://singular.rmrk.app/"

driver = webdriver.Chrome(r"../thetadrop/chromedriver.exe", chrome_options=chrome_options)

driver.get(NFT_link)

# login section
email = os.environ.get('thetadrop_email')
password = os.environ.get('thetadrop_pass')


def login(email, password):
    driver.implicitly_wait(10)
    login = driver.find_element(By.XPATH, "//button[normalize-space()='Login']")
    login.click()
    driver.implicitly_wait(10)
    email_input = driver.find_element(By.XPATH, "//input[@placeholder='email or username']")
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='password']")
    email_input.send_keys(email)
    password_input.send_keys(password)


try:
    login(email, password)
    print(input("Enter after logging in >> "))


except NoSuchElementException:
    print("Already logged in")


select_buy_xpath = "//button[normalize-space()='Select and buy']"
buy_button_xpath = "//button[@class='btn l green action-button']"
pay_with_tfuel_xpath = "//button[normalize-space()='Pay with TFuel']"


def buy_nft(select_and_buy, buy_button, pay_button, price):
    select_buy_button = driver.find_element(By.XPATH, select_and_buy)
    select_buy_button.click()
    radio_select = driver.find_element(By.XPATH, f"//strong[normalize-space()='${price}']")
    radio_elm_price = radio_select.text
    radio_elm_price_text = radio_elm_price.replace("$", "")
    radio_select.click()

    if float(radio_elm_price_text) == float(price):
        print(f"Current price({radio_elm_price}) and buying price({price}) are equal")
        buy_button = driver.find_element(By.XPATH, buy_button)
        buy_button.click()
        pay_button = driver.find_element(By.XPATH, pay_button)
        pay_button.click()

    elif float(radio_elm_price_text) > float(price):
        print("Price changed, skipping item")

    else:
        winsound.PlaySound("alarm.wav", winsound.SND_ASYNC)
        print("Something went wrong! contact developer")


def nft_search(price_xpath):
    for i in range(10000):
        driver.get(NFT_link)
        driver.implicitly_wait(10)
        price_value_elements = driver.find_elements(By.XPATH, price_xpath)
        for i in price_value_elements:
            nft_price = i.text
            dollar_nft_price = nft_price.replace("$", "")
            new_nft_price = dollar_nft_price.replace(",", "")
            if float(new_nft_price) < float(buying_price):
                i.click()
                buy_nft(select_and_buy=select_buy_xpath, buy_button=buy_button_xpath,pay_button=pay_with_tfuel_xpath,
                        price=new_nft_price)
                time.sleep(5)
                break
            else:
                print(f"{new_nft_price} $ price is bigger than {buying_price} $")

        time.sleep(4)


price_value_xpath = "//strong[@class='price-value']"

nft_search(price_value_xpath)

print(input("Element End .. :"))