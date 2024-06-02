import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def make_data_to_dataframe(data):
    df = pd.DataFrame(data)
    df["Дата"] = pd.to_datetime(df["Дата"], format="%m.%d.%Y")
    return df


def animate(frame, df, axis, type_inf):
    axis.clear()
    sns.lineplot(x="Дата", y=type_inf, data=df.iloc[:frame + 1], ax=axis)
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha="right")
    match type_inf:
        case "Количество заболевших":
            axis.set_title("График заболеваемости COVID-19")
        case "Количество умерших":
            axis.set_title("График смертности от COVID-19")
        case "Количество выздоровевших":
            axis.set_title("График выздоровлений от COVID-19")


def make_figure():
    fig, ax = plt.subplots()
    return fig, ax


def start_animation(fig, axis, df, type_inf):
    anim = FuncAnimation(fig, animate, frames=len(df), fargs=(df, axis, type_inf), interval=500, repeat=False)
    return anim
