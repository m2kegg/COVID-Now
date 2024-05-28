from datetime import date, datetime

import requests
from bs4 import BeautifulSoup


def get_сurrent_data():
    filter = ['Москва', 'Московская область', 'Белгородская область', 'Брянская область', 'Владимирская область',
              'Воронежская область', 'Ивановская область', 'Калужская область', 'Костромская область', 'Курская область'
                                                                                                       'Орловская область',
              'Рязанская область', 'Смоленская область', 'Тамбовская область',
              'Тверская область', 'Тульская область', 'Ярославская область', 'Липецкая область', ]

    url_stat = "https://russian-trade.com/coronavirus-russia/"  # откуда берём данные
    response = requests.get(url_stat)

    result_data = []
    page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга
    table = page.find('table', class_='grid_exch')  # получили таблицу с данными
    for data in table:
        if data.find("th") is not None and data.find(
                "th") != -1:  # Выбрасываем первую строку таблицы (с названиям полей)
            continue
        if data.find("a") != -1:  # Выбрасываем строки вида \n
            dict_covid = {}
            if data.find("a").string in filter:  # Проверка на нахождение региона в ЦФО:
                data_all = data.find_all("td")
                print(data_all)
                dict_covid["Регион"] = data.find("a").string
                dict_covid["Количество заболевших"] = int(data_all[2].contents[0])
                # dict_covid["Количество заболевших (отн)"] = int(data_all[2].contents[2].contents[0][1:-1])
                dict_covid["Количество умерших"] = int(data_all[3].contents[0])
                # dict_covid["Количество умерших (отн)"] = int(data_all[3].contents[2].contents[0][1:-1])
                dict_covid["Количество выздоровевших"] = int(data_all[4].contents[0])
                # dict_covid["Количество выздоровевших (отн)"] = int(data_all[4].contents[2].contents[0][1:-1])
                dict_covid["Количество оставшихся заболевших"] = int(data_all[5].contents[0])
                # dict_covid["Количество оставшихся заболевших (отн)"] = int(data_all[5].contents[2].contents[0][1:-1])
                result_data.append(dict_covid)
    return result_data


def get_data_by_day(day_request):
    filter = ['Москва', 'Московская область', 'Белгородская область', 'Брянская область', 'Владимирская область',
              'Воронежская область', 'Ивановская область', 'Калужская область',
              'Костромская область', 'Курская область''Орловская область',
              'Рязанская область', 'Смоленская область', 'Тамбовская область',
              'Тверская область', 'Тульская область', 'Ярославская область', 'Липецкая область', ]

    url_main = "https://russian-trade.com/coronavirus-russia/"
    url_reg = "https://russian-trade.com"

    response = requests.get(url_main)
    result_data = []
    page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга
    table = page.find('table', class_='grid_exch')  # получили таблицу с данными
    for data in table:
        if data.find("th") is not None and data.find(
                "th") != -1:  # Выбрасываем первую строку таблицы (с названиям полей)
            continue
        if data.find("a") != -1:  # Выбрасываем строки вида \n
            dict_covid = {}
            if data.find("a").string in filter:  # Проверка на нахождение региона в ЦФО:
                href = url_reg + data.find("a")['href']  # Ссылка на подробную статистику
                response_reg = requests.get(href)
                reg_data = BeautifulSoup(response_reg.text, 'html.parser')
                table_reg = reg_data.find('table')
                for data_1 in table_reg:
                    if len(data_1.find_all("td")) != 0:
                        date_reg = data_1.find_all('td')[0].text
                        date_reg_format = datetime.strptime(date_reg, '%d.%m.%Y')
                        if date_reg_format == day_request:
                            dict_covid["Регион"] = data.find("a").string
                            dict_covid["Количество заболевших"] = int(data_1.find_all('td')[1].text)
                            dict_covid["Количество умерших"] = int(data_1.find_all('td')[2].text)
                            dict_covid["Количество выздоровевших"] = int(data_1.find_all('td')[3].text)
                            dict_covid["Количество оставшихся заболевших"] = int(data_1.find_all('td')[4].text)
                            result_data.append(dict_covid)
    return result_data


def get_data_by_region(reg, last_10_days=False, day_request=date.today()):
    url_main = "https://russian-trade.com/coronavirus-russia/"
    url_reg = "https://russian-trade.com"
    response = requests.get(url_main)
    page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга
    table = page.find('table', class_='grid_exch')
    obrab = []
    for data in table.find_all('tr')[1:]:
        reg_get = data.find_all('td')[1].text
        if reg_get == reg:
            obrab = data.find_all('td')
    if last_10_days:
        href = url_reg + obrab[1].find('a')['href']
        response_reg = requests.get(href)
        reg_data = BeautifulSoup(response_reg.text, 'html.parser')
        table_reg = reg_data.find('table')
        res = []
        for data_1 in table_reg.find_all("tr")[:11]:
            dict_covid = {}
            data_obr = data_1.find_all("td")
            if len(data_obr) != 0:
                dict_covid["Дата"] = datetime.strptime(data_obr[0].text, "%d.%m.%Y")
                dict_covid["Количество заболевших"] = int(data_obr[1].text)
                dict_covid["Количество умерших"] = int(data_obr[2].text)
                dict_covid["Количество выздоровевших"] = int(data_obr[3].text)
                dict_covid["Количество оставшихся заболевших"] = int(data_obr[4].text)
                res.append(dict_covid)
    else:
        href = url_reg + obrab[1].find('a')['href']
        response_reg = requests.get(href)
        reg_data = BeautifulSoup(response_reg.text, 'html.parser')
        table_reg = reg_data.find('table')
        res = []
        for data_1 in table_reg.find_all("tr"):
            dict_covid = {}
            data_obr = data_1.find_all("td")
            if len(data_obr) != 0 and datetime.strptime(data_obr[0].text, "%d.%m.%Y") == day_request:
                dict_covid["Дата"] = datetime.strptime(data_obr[0].text, "%d.%m.%Y")
                dict_covid["Количество заболевших"] = int(data_obr[1].text)
                dict_covid["Количество умерших"] = int(data_obr[2].text)
                dict_covid["Количество выздоровевших"] = int(data_obr[3].text)
                dict_covid["Количество оставшихся заболевших"] = int(data_obr[4].text)
                res.append(dict_covid)
    return res


# Получает новости и выводит заголовки в список
def get_news():
    res = []
    for i in range(1, 4):
        url_main = f"https://объясняем.рф/stopkoronavirus/?PAGEN_1={i}"
        response = requests.get(url_main)
        page = BeautifulSoup(response.text, 'html.parser')
        news_first = page.find_all('a', class_='u-material-card u-material-cards__card')
        for news in news_first:
            text = news.find('h3').text.strip()
            if not "В России за неделю" in text:
                res.append(text)
    return res
