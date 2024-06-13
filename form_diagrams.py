"""
Модуль для работы с графиками Seaborn от полученных данных
"""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from screeninfo import get_monitors

def do_graph(df, axis, type_inf, color, font_size):
    """
    Функция, формирующая линейный график по датафрейму

    Параметр df - датафрейм Pandas, содержащий в себе колонки "Дата",
    "Количество заболевших", "Количество умерших", "Количество выздоровевших"

    Параметр axis - ось графика (формируется через make_figure)

    Параметр type_inf - по какой колонке строить график (строка, возможные значения -
    "Количество заболевших", "Количество умерших", "Количество выздоровевших")

    Параметр color - цвет графика (строка, задаётся через HEX или названием цвета на англ.

    Параметр font_size - размер шрифта для графика
    """

    if len(df) > 834:
        df = df.drop([834]) # фикс неприятного бага
    sns.lineplot(x="Дата", y=type_inf, data=df, ax=axis, color=color)
    axis.tick_params(axis='x', rotation=45)
    axis.set_xlabel("Дата", fontsize=font_size)
    axis.set_ylabel(type_inf, fontsize=font_size)


    axis.set_xticklabels(axis.get_xticklabels(), fontsize=font_size)
    axis.set_yticklabels(axis.get_yticklabels(), fontsize=font_size)

    axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".\
                                                     format(int(x)).replace(',', ' ')))

    match type_inf:
        case "Количество заболевших":
            axis.set_title("График заболеваемости COVID-19", fontsize=font_size)
        case "Количество умерших":
            axis.set_title("График смертности от COVID-19", fontsize=font_size)
        case "Количество выздоровевших":
            axis.set_title("График выздоровлений от COVID-19", fontsize=font_size)

def make_figure(figsize=(5, 3.5)):
    """
    Функция, задающая размер графика (фигуру) и оси графика

    Параметр figsize - размер графика: кортеж вида (длина, ширина) в дюймах

    Возвращает фигуру и ось графика
    """
    fig, ax = plt.subplots(figsize=figsize)

    return fig, ax

def get_font_size(width, height):
    base_size = 8
    scale = min(width, height) / 400
    return int(base_size * scale)


def create_and_place_graph(df, y_column, frame, color):
    """
    Функция, размещаюшая график непосредственно на фрейме

    Параметр df - датафрейм Pandas, содержащий в себе колонки "Дата",
    "Количество заболевших", "Количество умерших", "Количество выздоровевших"

    Параметр y_column - по какой колонке строить график (строка, возможные значения -
    "Количество заболевших", "Количество умерших", "Количество выздоровевших")

    Параметр frame - в каком фрейме необходимо разместить график (объект CTKFrame)

    Параметр color - цвет графика (строка, задаётся через HEX или названием цвета на англ.
    """
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    font_size = get_font_size(frame_width, frame_height) * 1.3
    fig, ax = make_figure(figsize=(frame_width / 100, frame_height / 100))
    do_graph(df, ax, y_column, color, font_size)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=1)
    canvas.draw()
