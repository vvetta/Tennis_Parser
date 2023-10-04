import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from settings import PATH_TO_WEBDRIVER, PARS_URL
from selenium.webdriver.chrome.options import Options


def _get_table_rows(driver):

    result = driver.find_element(By.CLASS_NAME, "tpBody")
    number = driver.find_elements(By.CLASS_NAME, "tpRow")

    return result, len(number)
    


def parser():
    # options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome()
    list_result = []
    driver.get(PARS_URL)
    time.sleep(2)

    while True:
        time.sleep(0.4)

        result, get_number = _get_table_rows(driver)

        soup = BeautifulSoup(result.get_attribute("outerHTML"), "html.parser")
        table_cells = soup.findAll('tr')

        for data in table_cells:
            cells = data.find_all('td')
            list_result.append({
                "Место": cells[0].text,
                "ФИО": cells[1].text,
                "Пол игрока": cells[2].text,
                "РНИ": cells[3].text,
                "Дата рождения": cells[4].text,
                "Город": cells[5].text,
                "Количество турниров за 52 недели": cells[6].text,
                "Из них зачётных": cells[7].text,
                "Возрастная группа": cells[8].text,
                "Очки": cells[9].text,
                "Оплата за 2023 год": cells[10].text})
            
        if get_number < 25:
            break

        btn_next = driver.find_element(By.LINK_TEXT, "››")
        btn_next.click()
        print(type(table_cells))

    for row in list_result:
        print(row, '\n')


if __name__ == "__main__":
    parser()

