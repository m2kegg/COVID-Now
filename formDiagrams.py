import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def make_data_to_dataframe(data):
    df = pd.DataFrame(data)
    df["Дата"] = pd.to_datetime(df["Дата"], format="%m.%d.%Y")
    return df


def do_graph(df, axis, type_inf, color):
    if len(df) > 834:
        df = df.drop([834])
    sns.lineplot(x="Дата", y=type_inf, data=df, ax=axis, color=color)
    axis.tick_params(axis='x', rotation=45)

    axis.set_xticklabels(axis.get_xticklabels(), fontsize=8)
    axis.set_yticklabels(axis.get_yticklabels(), fontsize=8)

    axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)).replace(',', ' ')))

    match type_inf:
        case "Количество заболевших":
            axis.set_title("График заболеваемости COVID-19")
        case "Количество умерших":
            axis.set_title("График смертности от COVID-19")
        case "Количество выздоровевших":
            axis.set_title("График выздоровлений от COVID-19")


def make_figure(figsize=(5, 3.5)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def create_and_place_graph(df, y_column, frame, color):
    fig, ax = make_figure()
    do_graph(df, ax, y_column, color)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=1)
    canvas.draw()