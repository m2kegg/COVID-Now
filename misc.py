from datetime import datetime

# функция для замены сепаратора на пробел
def format_with_space_separator(value):
    return f"{value:,}".replace(',', ' ')


# функция, очищающая фрейм
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# функция для проверки активности дня
def is_day_exist(day: int, month: int, year: int):
    now_date = datetime(year, month, day)
    if now_date < datetime(2020, 3, 27) or now_date > datetime.today():
        return "disabled"
    if now_date <= datetime(2023, 5, 15):
        return "normal"
    if now_date > datetime(2023, 5, 16) and now_date.weekday() == 1:
        return "normal"
    return "disabled"

