import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from settings import PATH_TO_WEBDRIVER, PARS_URL


def parser():
    driver = webdriver.Chrome()
    driver.get(PARS_URL)
    time.sleep(2)

    while True:
        time.sleep(0.15)
        btn_next = driver.find_element(By.LINK_TEXT, "››")
        btn_next.click()




if __name__ == "__main__":
    parser()

