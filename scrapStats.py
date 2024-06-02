import locale
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, UniqueConstraint, select
from dateutil.parser import parse

import requests
from bs4 import BeautifulSoup


def get_сurrent_data():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    filter = ['Москва', 'Московская область', 'Белгородская область', 'Брянская область', 'Владимирская область',
              'Воронежская область', 'Ивановская область', 'Калужская область',
              'Костромская область', 'Курская область', 'Орловская область',
              'Рязанская область', 'Смоленская область', 'Тамбовская область',
              'Тверская область', 'Тульская область', 'Ярославская область', 'Липецкая область']

    url_stat = "https://russian-trade.com/coronavirus-russia/"  # откуда берём данные
    response = requests.get(url_stat)

    result_data = []
    page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга

    # Неприятное преобразование данных
    translation = {"января": "janyary", "февраля": "february", "марта": "march", "апреля": "april", "мая": "may",
                   "июня": 'june', "июля": "july", "августа": "august", "сентября": "september", "октября": "october",
                   "ноября": "november",
                   "декабря": "december"}

    date_last = page.find_all('p')[2].find('span').string
    date_last = date_last.replace(" года", "")
    date_last = date_last.split()
    date_last[1] = translation[date_last[1]]
    date_last = "".join(date_last)
    date_object = parse(date_last).date()

    table = page.find('table', class_='grid_exch')  # получили таблицу с данными
    for data in table:
        if data.find("th") is not None and data.find(
                "th") != -1:  # Выбрасываем первую строку таблицы (с названиям полей)
            continue
        if data.find("a") != -1:  # Выбрасываем строки вида \n
            dict_covid = {}
            if data.find("a").string in filter:  # Проверка на нахождение региона в ЦФО:
                data_all = data.find_all("td")
                dict_covid["Дата"] = date_object
                dict_covid["Регион"] = data.find("a").string
                dict_covid["Количество заболевших"] = int(data_all[2].contents[0])
                dict_covid["Количество умерших"] = int(data_all[3].contents[0])
                dict_covid["Количество выздоровевших"] = int(data_all[4].contents[0])
                dict_covid["Количество оставшихся заболевших"] = int(data_all[5].contents[0])
                result_data.append(dict_covid)
    return result_data


def get_data():
    filter = ['Москва', 'Московская область', 'Белгородская область', 'Брянская область', 'Владимирская область',
              'Воронежская область', 'Ивановская область', 'Калужская область',
              'Костромская область', 'Курская область', 'Орловская область',
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
            if data.find("a").string in filter:  # Проверка на нахождение региона в ЦФО:
                href = url_reg + data.find("a")['href']  # Ссылка на подробную статистику
                response_reg = requests.get(href)
                reg_data = BeautifulSoup(response_reg.text, 'html.parser')
                table_reg = reg_data.find('table')
                for data_1 in table_reg:
                    if len(data_1.find_all("td")) != 0:
                        dict_covid = {}
                        date_reg = data_1.find_all('td')[0].text
                        date_reg_format = datetime.strptime(date_reg, '%d.%m.%Y')
                        dict_covid["Регион"] = data.find("a").string
                        dict_covid["Дата"] = date_reg_format.date()
                        dict_covid["Количество заболевших"] = int(data_1.find_all('td')[1].text)
                        dict_covid["Количество умерших"] = int(data_1.find_all('td')[2].text)
                        dict_covid["Количество выздоровевших"] = int(data_1.find_all('td')[3].text)
                        dict_covid["Количество оставшихся заболевших"] = int(data_1.find_all('td')[4].text)
                        result_data.append(dict_covid)
    return result_data


def write_to_db(data):
    engine = create_engine('sqlite:///data_covid.db')

    meta = MetaData()

    table_data = Table('covid_data', meta,
                       Column('id', Integer, primary_key=True),
                       Column('Регион', String, nullable=False),
                       Column('Дата', Date, nullable=False),
                       Column("Количество заболевших", Integer, nullable=False),
                       Column("Количество умерших", Integer, nullable=False),
                       Column("Количество выздоровевших", Integer, nullable=False),
                       Column("Количество оставшихся заболевших", Integer, nullable=False),
                       )

    meta.create_all(engine)

    with engine.connect() as conn:
        conn.execute(table_data.insert(), data)
        conn.commit()


def get_all_data_db(date_chosen):
    engine = create_engine('sqlite:///data_covid.db')
    meta = MetaData()
    table = Table('covid_data', meta, autoload_with=engine)
    with engine.connect() as conn:
        query = select(table).where(table.c.Дата <= date_chosen)
        res = conn.execute(query).mappings().all()
    return res


def get_reg_data_db(reg, date_chosen = date.today(), last_10_days=True):
    if last_10_days:
        engine = create_engine('sqlite:///data_covid.db')
        meta = MetaData()
        table = Table('covid_data', meta, autoload_with=engine)
        with engine.connect() as conn:
            query_extra = select(table).order_by(table.c.id).limit(1)
            date_end = conn.execute(query_extra).mappings().all()[0]["Дата"]
            date_start = date_end - timedelta(days=10)
            query = select(table).where(table.c.Дата.between(date_start, date_end)).where(table.c.Регион == reg)
            res = conn.execute(query).mappings().all()
            return res
    else:
        engine = create_engine('sqlite:///data_covid.db')
        meta = MetaData()
        table = Table('covid_data', meta, autoload_with=engine)
        with engine.connect() as conn:
            query = select(table).where(table.c.Дата <= date_chosen).where(table.c.Регион == reg)
            res = conn.execute(query).mappings().all()
            return res



# def get_data_by_region(reg, last_10_days=False, day_request=date.today()):
#     url_main = "https://russian-trade.com/coronavirus-russia/"
#     url_reg = "https://russian-trade.com"
#     response = requests.get(url_main)
#     page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга
#     table = page.find('table', class_='grid_exch')
#     obrab = []
#     for data in table.find_all('tr')[1:]:
#         reg_get = data.find_all('td')[1].text
#         if reg_get == reg:
#             obrab = data.find_all('td')
#     if last_10_days:
#         href = url_reg + obrab[1].find('a')['href']
#         response_reg = requests.get(href)
#         reg_data = BeautifulSoup(response_reg.text, 'html.parser')
#         table_reg = reg_data.find('table')
#         res = []
#         for data_1 in table_reg.find_all("tr")[:11]:
#             dict_covid = {}
#             data_obr = data_1.find_all("td")
#             if len(data_obr) != 0:
#                 dict_covid["Дата"] = datetime.strptime(data_obr[0].text, "%d.%m.%Y")
#                 dict_covid["Количество заболевших"] = int(data_obr[1].text)
#                 dict_covid["Количество умерших"] = int(data_obr[2].text)
#                 dict_covid["Количество выздоровевших"] = int(data_obr[3].text)
#                 dict_covid["Количество оставшихся заболевших"] = int(data_obr[4].text)
#                 res.append(dict_covid)
#     else:
#         href = url_reg + obrab[1].find('a')['href']
#         response_reg = requests.get(href)
#         reg_data = BeautifulSoup(response_reg.text, 'html.parser')
#         table_reg = reg_data.find('table')
#         res = []
#         for data_1 in table_reg.find_all("tr"):
#             dict_covid = {}
#             data_obr = data_1.find_all("td")
#             if len(data_obr) != 0 and datetime.strptime(data_obr[0].text, "%d.%m.%Y") == day_request:
#                 dict_covid["Дата"] = datetime.strptime(data_obr[0].text, "%d.%m.%Y")
#                 dict_covid["Количество заболевших"] = int(data_obr[1].text)
#                 dict_covid["Количество умерших"] = int(data_obr[2].text)
#                 dict_covid["Количество выздоровевших"] = int(data_obr[3].text)
#                 dict_covid["Количество оставшихся заболевших"] = int(data_obr[4].text)
#                 res.append(dict_covid)
#     return res


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
