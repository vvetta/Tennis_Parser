import time
from settings import PARS_URL
from typing import NamedTuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class TableRowsResult(NamedTuple):
    result: WebElement
    number_of_table_rows: int


def init_parser(url: str, link_text_pagination_btn: str, options: Options=None) -> WebDriver:
    """
    En: Initialization of the parser. Returns an instance of the WebDriver class.

    Ru: Инициализация парсера. Возвращает экземпляр класса WebDriver.
    """

    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    wait = WebDriverWait(driver, 100, ignored_exceptions=StaleElementReferenceException)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, link_text_pagination_btn)))

    return driver


def _get_table_and_table_rows(driver: WebDriver,
                              class_of_table: str, 
                              class_of_rows: str) -> TableRowsResult:
    """
    En: Gets an instance of the WebDriver class, 
    Css table class and Css row class, returns the table and the number of rows.

    Ru: Принимает экземпляр класса WebDriver, 
    Css класс таблицы и Css класс строки, возвращает таблицу и количество строк.
    """

    wait = WebDriverWait(driver, 100, ignored_exceptions=StaleElementReferenceException)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_of_table)))

    parsing_table = driver.find_element(By.CLASS_NAME, class_of_table)
    number_of_rows = len(driver.find_elements(By.CLASS_NAME, class_of_rows))

    return TableRowsResult(parsing_table, number_of_rows)


def _get_table_rows_html(parsing_table: WebElement, tag_of_rows: str) -> list:
    """
    En: Retrieves the saved table and the Css class of rows of this table,
    returns a list of rows of this table

    Ru: Получает спарсенную таблицу и Css класс строк этой таблицы, 
    возвращает список строк этой таблицы
    """

    soup = BeautifulSoup(parsing_table.get_attribute("outerHTML"), "html.parser")
    table_rows = soup.findAll(tag_of_rows)

    return table_rows


def _paginate(driver: WebDriver, location_method: str, value: str) -> None:
    """
    En: Accepts an instance of the WebDriver class, the method, 
    which will be used to search for the pagination button and the value itself.

    Ru: Принимет экземпляр класс WebDriver, метод, 
    по которому будет происходить поиск кнопки пагинации и само значение.
    """

    match location_method:
        case "LINK_TEXT":
            btn_next = driver.find_element(By.LINK_TEXT, value)
        case "XPATH":
            btn_next = driver.find_element(By.LINK_TEXT, value)
        case "CSS_SELECTOR":
            btn_next = driver.find_element(By.CSS_SELECTOR, value)
        case "CLASS_NAME":
            btn_next = driver.find_element(By.CLASS_NAME, value)
        case "ID":
            btn_next = driver.find_element(By.ID, value)
        case "NAME":
            btn_next = driver.find_element(By.NAME, value)
        case "TAG_NAME":
            btn_next = driver.find_element(By.TAG_NAME, value)
        case "PARTIAL_LINK_TEXT":
            btn_next = driver.find_element(By.PARTIAL_LINK_TEXT, value)
        case _:
            print("Такого метода нет.")
    
    btn_next.click()


def _format_result_data(table_rows: list, tag_of_cell: str, formater_text: list) -> list:
    """
    En: Gets a date as a list, formats it, and returns a dictionary.

    Ru: Принимает дату в виде списка, форматирует и возвращает словарь.
    """

    for row in table_rows:
        cells = row.find_all(tag_of_cell)
        formater_text.append({
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
                "Оплата за 2023 год": cells[10].text
            })
        
    return formater_text


def _wait_load_rows(driver: WebDriver, class_of_rows: str) -> None:
    """
    En: Checks whether the table page has loaded after pagination.

    Ru: Смотрит загрузилась ли страница таблицы после пагинации.
    """

    wait = WebDriverWait(driver, 100, ignored_exceptions=StaleElementReferenceException)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_of_rows)))
    time.sleep(0.2)


def parser() -> list:
    """
    En: The function where the main work of the parser takes place is
    here pagination occurs and all nested functions are called,
    returns a ready list with all the table information.

    Ru: Функция, в которой происходит основная работа парсера, 
    тут происходит пагинация и вызов всех вложенных функций, 
    возвращает готовый список со всей информацией таблицы.
    """

    # options = Options()
    # options.add_argument("--headless")
    
    driver = init_parser(PARS_URL, "››")

    result_list = []
    formater_text = []

    while True:
        _wait_load_rows(driver, "tpRow")

        parsing_table, number_of_rows = _get_table_and_table_rows(driver, "tpBody", "tpRow")

        result = (_format_result_data(_get_table_rows_html(parsing_table, tag_of_rows="tr"), 
                            tag_of_cell="td", formater_text=formater_text))
        
        if number_of_rows < 25:
            break

        _paginate(driver, "LINK_TEXT", "››")
    
    result_list.append(result)
    
    return result_list[0]


if __name__ == "__main__":
    parser()

