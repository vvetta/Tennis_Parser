import requests
from bs4 import BeautifulSoup


base_url = "https://www.rustennistur.ru/csp/rtt/RTTXEN.RatingTable.cls"
function_name = 'return zenPage.getComponent(9).gotoPage(2);'
page_number = 2

url = f'{base_url}?onmousedown={function_name}'

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

table_rows = []
table_rows = soup.findAll('tr', class_='tpRow')

result = []

for data in table_rows:
    cells = data.find_all('td')
    result.append({
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

for row in result:
    print(row, '\n')