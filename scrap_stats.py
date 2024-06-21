"""
Модуль для работы с сайтом Внешней торговли РФ (статистика),
объясняем.рф (новости) и для работы с базой данных SQLite

Функции:
    get_current_data()
    get_data()
    write_to_db(data)
    get_all_data_db(date_chosen)
    get_reg_data_db(reg, date_chosen=date.today(), last_10_writes=False)
    get_today_data_db()
    check_has_in_base(data)
    get_news()
    check_has_in_base(data)
    perform_check(ctk)
"""

from datetime import date, datetime, timedelta
from urllib.error import URLError
from urllib.request import urlopen

from sqlalchemy import create_engine, MetaData, Table, select
from dateutil.parser import parse


import requests
from bs4 import BeautifulSoup


def get_current_data():
    """
    Функция, получающая данные статистики по ковиду на последнее число.
    Возвращает список словарей с ключами "Дата" (datetime), "Регион" (строка),
    "Количество заболевших" (число), "Количество умерших" (число),
    "Количество оставшихся заболевших" (число)
    """

    filter_reg = ['Москва', 'Московская область',
                  'Белгородская область', 'Брянская область', 'Владимирская область',
                  'Воронежская область', 'Ивановская область', 'Калужская область',
                  'Костромская область', 'Курская область', 'Орловская область',
                  'Рязанская область', 'Смоленская область', 'Тамбовская область',
                  'Тверская область', 'Тульская область', 'Ярославская область', 'Липецкая область']

    url_stat = "https://russian-trade.com/coronavirus-russia/"  # откуда берём данные
    response = requests.get(url_stat, timeout=10)

    result_data = []
    page = BeautifulSoup(response.text, 'html.parser')  # получили страницу для парсинга

    # Неприятное преобразование данных
    translation = {"января": "janyary", "февраля": "february",
                   "марта": "march", "апреля": "april", "мая": "may",
                   "июня": 'june', "июля": "july", "августа": "august",
                   "сентября": "september", "октября": "october",
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
            if data.find("a").string in filter_reg:  # Проверка на нахождение региона в ЦФО:
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
    """
    Функция, получающая полную статистику о ковиде за всё время наблюдений в ЦФО.
    Без крайней нужды не вызывать, поскольку работает долго. Возвращает список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число),  "Количество оставшихся заболевших" (число)
    """

    filter_reg = ['Москва', 'Московская область',
                  'Белгородская область', 'Брянская область', 'Владимирская область',
                  'Воронежская область', 'Ивановская область', 'Калужская область',
                  'Костромская область', 'Курская область', 'Орловская область',
                  'Рязанская область', 'Смоленская область', 'Тамбовская область',
                  'Тверская область', 'Тульская область', 'Ярославская область', 'Липецкая область']

    url_main = "https://russian-trade.com/coronavirus-russia/"
    url_reg = "https://russian-trade.com"

    response = requests.get(url_main, timeout=10)
    result_data = []
    table = BeautifulSoup(response.text, 'html.parser'). \
        find('table', class_='grid_exch')  # получили таблицу с данными
    for data in table:
        if data.find("th") is not None and data.find(
                "th") != -1:  # Выбрасываем первую строку таблицы (с названиям полей)
            continue
        if data.find("a") != -1:  # Выбрасываем строки вида \n
            if data.find("a").string in filter_reg:  # Проверка на нахождение региона в ЦФО:
                href = url_reg + data.find("a")['href']  # Ссылка на подробную статистику
                response_reg = requests.get(href, timeout=10)
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
                        dict_covid["Количество оставшихся заболевших"] = \
                            int(data_1.find_all('td')[4].text)
                        result_data.append(dict_covid)
    return result_data


def write_to_db(data):
    """
    Функция, проводящая запись в базу данных
    Параметр data - список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число),  "Количество оставшихся заболевших" (число)
    """
    engine = create_engine('sqlite:///data_covid.db')

    meta = MetaData()

    table_data = Table('covid_data', meta, autoload_with=engine)

    meta.create_all(engine)

    with engine.connect() as conn:
        conn.execute(table_data.insert(), data)
        conn.commit()


def get_all_data_db(date_chosen):
    """
    Функция, получающая все данные по ковиду по заданное число
    Параметр date_chosen - дата в формате datetime (по какую дату нужна статистика)
    Возвращает список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число),  "Количество оставшихся заболевших" (число)
    """
    engine = create_engine('sqlite:///data_covid.db')
    meta = MetaData()
    table = Table('covid_data', meta, autoload_with=engine)
    with engine.connect() as conn:
        query = select(table).where(table.c.Дата <= date_chosen)
        res = conn.execute(query).mappings().all()
    return res


def get_reg_data_db(reg, date_chosen=date.today(), last_10_writes=False):
    """
    Функция, получающая все данные по какое-либо число ИЛИ последние 10 записей

    Параметр reg (обязательный) - регион ЦФО (в формате строки)

    Параметр date_chosen (необязательный) - по какую дату необходимы данные

    Параметр last_10_writes - выборка последних 10 записей

    Возвращает список словарей с ключами "Дата" (datetime),
    "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число),  "Количество оставшихся заболевших" (число)
    """
    if last_10_writes:
        engine = create_engine('sqlite:///data_covid.db')
        meta = MetaData()
        table = Table('covid_data', meta, autoload_with=engine)
        with engine.connect() as conn:
            query_extra = select(table).order_by(table.c.id).limit(1)
            date_end = conn.execute(query_extra).mappings().all()[0]["Дата"]
            date_start = date_end - timedelta(days=69)
            query = select(table).where(table.c.Дата.between(date_start, date_end)).\
                where(table.c.Регион == reg)
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


def get_today_data_db():
    """
    Функция, получающая данные из базы данных на последнее число

    Возвращает список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число), "Количество оставшихся заболевших" (число)
    """
    engine = create_engine('sqlite:///data_covid.db')
    meta = MetaData()
    table = Table('covid_data', meta, autoload_with=engine)
    query = select(table.c.Дата).order_by(table.c.Дата.desc()).limit(1)
    with engine.connect() as conn:
        res_data = conn.execute(query).mappings().all()[0]["Дата"]
        query_main = select(table).where(table.c.Дата == res_data)
        res = conn.execute(query_main).mappings().all()
        return res

def get_two_dates_db(reg, date_first, date_second):
    """
    Функция, получающая данные из базы данных по региону между двумя датами

    Возвращает список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число), "Количество оставшихся заболевших" (число)
    """
    engine = create_engine('sqlite:///data_covid.db')
    meta = MetaData()
    table = Table('covid_data', meta, autoload_with=engine)
    query = select(table).where(date_first <= table.c.Дата).where(table.c.Дата <= date_second).where(table.c.Регион == reg)
    with engine.connect() as conn:
        res = conn.execute(query).mappings().all()
        return res

def check_has_in_base(data):
    """
    Функция, проверяющая наличие записи в базе данных

    Параметр data: - список словарей с ключами
    "Дата" (datetime), "Регион" (строка), "Количество заболевших" (число),
    "Количество умерших" (число),  "Количество оставшихся заболевших" (число)

    Возвращает True при наличии такой записи, иначе - False
    """
    engine = create_engine('sqlite:///data_covid.db')
    meta = MetaData()
    table = Table('covid_data', meta, autoload_with=engine)
    query = select(table).filter_by(Дата=data[0]["Дата"]).limit(1)
    with engine.connect() as conn:
        res = conn.execute(query).mappings().all()
        if len(res) == 0:
            return False
        return True


def perform_check(ctk):
    """
    Функция, проверяющая подключение к интернету

    Параметр ctk - объект вида CTk (необходим для отображения уведомления
    об отсутствии подключения к интернету
    """
    if date.today().weekday() == 4:
        try:
            urlopen("https://www.google.com", timeout=5)
            data_last = get_current_data()
            if not check_has_in_base(data_last):
                write_to_db(data_last)
        except URLError:
            warning_window = ctk.CTkTopLevel()
            warning_window.title("Внимание")
            warning_window.geometry("300x150")

            label = ctk.CTkLabel(warning_window,
                text="Отсутствует подключение к интернету. Из-за этого данные будут неактуальными")
            label.pack(pady=20)

            button = ctk.CTkButton(warning_window, text="OK", command=warning_window.destroy)
            button.pack(pady=10)



def get_news():
    """
    Функция, получающая новости с сайта объясняем.рф

    Возвращает список с заголовками новостей (тип - строки)
    """
    res = []
    for i in range(1, 4):
        url_main = f"https://объясняем.рф/stopkoronavirus/?PAGEN_1={i}"
        response = requests.get(url_main, timeout=15)
        page = BeautifulSoup(response.text, 'html.parser')
        news_first = page.find_all('a', class_='u-material-card u-material-cards__card')
        for news in news_first:
            text = news.find('h3').text.strip()
            if not "В России за неделю" in text:
                res.append(text)
    return res
