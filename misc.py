"""
Модуль с различными функциями, необходимыми для работы приложения

Функции:
    format_with_space_separator(value)
    clear_frame(frame)
    is_day_exist(day: int, month: int, year: int)
"""

from datetime import datetime


def format_with_space_separator(value):
    """
    Функция, заменяющая сепаратор в строке на пробел

    Параметр value - строка, в которой необходима замена

    Возвращает изменённую строку
    """
    return f"{value:,}".replace(',', ' ')


def clear_frame(frame):
    """
    Функция, очищающая фрейм

    Параметр frame - объект вида CTkframe
    """
    for widget in frame.winfo_children():
        widget.destroy()


# функция для проверки активности дня
def is_day_exist(day: int, month: int, year: int):
    """
    Функция, проверяющая, есть ли данные на этот день

    Параметр day - день (число)

    Параметр month - месяц (число)

    Параметр year - год (число)
    """
    now_date = datetime(year, month, day)
    if now_date < datetime(2020, 3, 27) or now_date > datetime.today():
        return "disabled"
    if now_date <= datetime(2023, 5, 15):
        return "normal"
    if now_date > datetime(2023, 5, 16) and now_date.weekday() == 1:
        return "normal"
    return "disabled"
