"""
Модуль для работы с графиками Seaborn от полученных данных
"""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def do_graph(df, axis, type_inf, color):
    """
    Функция, формирующая линейный график по датафрейму

    Параметр df - датафрейм Pandas, содержащий в себе колонки "Дата",
    "Количество заболевших", "Количество умерших", "Количество выздоровевших"

    Параметр axis - ось графика (формируется через make_figure)

    Параметр type_inf - по какой колонке строить график (строка, возможные значения -
    "Количество заболевших", "Количество умерших", "Количество выздоровевших")

    Параметр color - цвет графика (строка, задаётся через HEX или названием цвета на англ.
    """

    if len(df) > 834:
        df = df.drop([834]) # фикс неприятного бага
    sns.lineplot(x="Дата", y=type_inf, data=df, ax=axis, color=color)
    axis.tick_params(axis='x', rotation=45)

    axis.set_xticklabels(axis.get_xticklabels(), fontsize=8)
    axis.set_yticklabels(axis.get_yticklabels(), fontsize=8)

    axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".\
                                                     format(int(x)).replace(',', ' ')))

    match type_inf:
        case "Количество заболевших":
            axis.set_title("График заболеваемости COVID-19")
        case "Количество умерших":
            axis.set_title("График смертности от COVID-19")
        case "Количество выздоровевших":
            axis.set_title("График выздоровлений от COVID-19")


def make_figure(figsize=(5, 3.5)):
    """
    Функция, задающая размер графика (фигуру) и оси графика

    Параметр figsize - размер графика: кортеж вида (длина, ширина) в дюймах

    Возвращает фигуру и ось графика
    """
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


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
    fig, ax = make_figure()
    do_graph(df, ax, y_column, color)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=1)
    canvas.draw()
