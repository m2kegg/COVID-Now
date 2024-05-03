from bs4 import BeautifulSoup
import requests


def getCurrentData():
    filter = ['Москва', 'Московская область', 'Белгородская область', 'Брянская область', 'Владимирская область',
              'Воронежская область', 'Ивановская область', 'Калужская область', 'Костромская область', 'Курская область'
                                                                                                       'Липецкая область',
              'Орловская область', 'Рязанская область', 'Смоленская область', 'Тамбовская область',
              'Тверская область', 'Тульская область', 'Ярославская область']

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
                dict_covid["Регион"] = data.find("a").string
                dict_covid["Количество заболевших (абс)"] = int(data_all[2].contents[0])
                dict_covid["Количество заболевших (отн)"] = int(data_all[2].contents[2].contents[0][1:-1])
                dict_covid["Количество умерших (абс)"] = int(data_all[3].contents[0])
                dict_covid["Количество умерших (отн)"] = int(data_all[3].contents[2].contents[0][1:-1])
                dict_covid["Количество выздоровевших (абс)"] = int(data_all[4].contents[0])
                dict_covid["Количество выздоровевших (отн)"] = int(data_all[4].contents[2].contents[0][1:-1])
                dict_covid["Количество оставшихся заболевших (абс)"] = int(data_all[5].contents[0])
                dict_covid["Количество оставшихся заболевших (отн)"] = int(data_all[5].contents[2].contents[0][1:-1])
                result_data.append(dict_covid)
    return result_data
