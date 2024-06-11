'''
 Про конфигурацию текста в прямоугольниках - теперь для каждого экрана есть свой собственный Label-объект
 с настроенной переменной. main_info_label -> main_info_text. При помощи метода .set для text переменных
 можно динамически менять содержание текста label без метода configure.
'''
import os
from calendar import monthrange
from datetime import datetime

import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import samples as sa
from scrapStats import *
from formDiagrams import *
from misc import *
from config import *

data_today = pd.DataFrame(get_today_data_db())
data_all = pd.DataFrame(get_all_data_db(date.today()))

# Проверка на нахождение в location-окне
is_in_3 = False

# Проверка на выделение чекбокса
has_checked = False

# Окно в данный момент
current_window = ""

sns.set_style('darkgrid')

# Расстановка графиков по фреймам
def place_all_graphs(df_to_graph):
    clear_frame(ill_chart_frame)
    clear_frame(death_chart_frame)
    clear_frame(cured_chart_frame)

    create_and_place_graph(df_to_graph[["Дата", "Количество заболевших"]], "Количество заболевших", ill_chart_frame,
                           "red")
    create_and_place_graph(df_to_graph[["Дата", "Количество умерших"]], "Количество умерших", death_chart_frame,
                           "blue")
    create_and_place_graph(df_to_graph[["Дата", "Количество выздоровевших"]], "Количество выздоровевших",
                           cured_chart_frame, "green")


def home_button_callback():
    global current_window
    current_window = "Home"
    home_button.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], image=home_img_a)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0, 1, 2), weight=0)
    info_frame.grid_columnconfigure(0, weight=0)

    info_frame.grid_rowconfigure(0, weight=1)
    info_frame.grid_columnconfigure(0, weight=1)

    main_info_label.tkraise()

    news_frame.grid(row=0, column=0, sticky="nsew")
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    calendar_frame.grid_remove()

    name_textbox_text.set(sa.home_main_text + f"{datetime.today().strftime('%d.%m.%Y')}")
    main_info_text.set(sa.frame_home_text.format(date_last_call=datetime.today().strftime('%d.%m.%y'),
                                                 num_diseased=data_today["Количество заболевших"].sum(),
                                                 num_cured=data_today["Количество выздоровевших"].sum(),
                                                 num_dead=data_today["Количество умерших"].sum(),
                                                 num_infected=data_today[
                                                     "Количество оставшихся заболевших"].sum()))
    main_info_label.configure(font=font_info)

    df_to_graph = data_all.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]].sum().reset_index()

    place_all_graphs(df_to_graph)


def cal_button_callback():
    global is_in_3, current_window
    is_in_3 = False
    current_window = "Calendar"
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(
        fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], image=cal_img_a)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0, 1, 2), weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    cal_info_label.tkraise()

    news_frame.grid_remove()
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    calendar_frame.grid_configure(
        row=0, column=0, padx=(10, 10), pady=(50, 0), sticky="new")

    filter_date = datetime(sa.year, sa.month, sa.day)

    if filter_date.weekday() != 1 and filter_date >= datetime(2023, 5, 16):
        day_of_week = filter_date.weekday()

        if day_of_week > 1:
            days_to_tuesday = day_of_week - 1
        else:
            days_to_tuesday = 6

        prev_tuesday = filter_date - timedelta(days=days_to_tuesday)

        sa.day = prev_tuesday.day
        sa.month = prev_tuesday.month
        sa.year = prev_tuesday.year

    name_textbox_text.set(sa.cal_main_text + '%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.day, 'month': sa.month, 'year': sa.year})

    data_on_date_all = pd.DataFrame(get_all_data_db(datetime(sa.year, sa.month, sa.day)))
    data_on_date_all['Дата'] = pd.to_datetime(data_on_date_all['Дата'])
    data_on_date = data_on_date_all[data_on_date_all['Дата'] == filter_date]

    cal_info_text.set(sa.frame_cal_text.format(date_last_call=datetime(sa.year, sa.month, sa.day).strftime('%d.%m.%y'),
                                               num_diseased=format_with_space_separator(
                                                   data_on_date["Количество заболевших"].sum()),
                                               num_cured=format_with_space_separator(
                                                   data_on_date["Количество выздоровевших"].sum()),
                                               num_dead=format_with_space_separator(
                                                   data_on_date["Количество умерших"].sum()),
                                               num_infected=format_with_space_separator(data_on_date[
                                                                                            "Количество оставшихся заболевших"].sum())))

    df_to_graph = data_on_date_all.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]].sum().reset_index()

    place_all_graphs(df_to_graph)


def loc_button_callback():
    global is_in_3, current_window
    is_in_3 = True
    current_window = "Location"
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(
        fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], image=loc_img_a)

    info_frame.grid_rowconfigure((0, 1, 2), weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    loc_info_label.tkraise()

    news_frame.grid_remove()

    loc_opt_menu.grid_configure(row=0, column=0, padx=(
        13, 13), pady=(33, 0), sticky="ew")
    last_ten_box.grid_configure(
        row=1, column=0, padx=(13, 13), pady=(40, 0), sticky="")
    calendar_frame.grid_configure(row=2, column=0, padx=(10, 10), pady=(50, 0), sticky="new")
    last_ten_box.deselect()
    last_ten_box.configure(command=last_ten_check_callback)

    name_textbox_text.set(sa.loc_main_text + loc_opt_menu.get() + " на " +
                          '%(day)02d.%(month)02d.%(year)d' % {'day': sa.day, 'month': sa.month, 'year': sa.year})

    data_on_date = pd.DataFrame(
        get_reg_data_db(loc_opt_menu.get(), date_chosen=datetime(sa.year, sa.month, sa.day)))

    data_on_date_chosen = data_on_date.iloc[0]
    loc_info_text.set(sa.frame_loc_text.format(date_last_call=datetime(sa.year, sa.month, sa.day).strftime('%d.%m.%y'),
                                               region=loc_opt_menu.get(),
                                               num_diseased=format_with_space_separator(
                                                   data_on_date_chosen["Количество заболевших"].sum()),
                                               num_cured=format_with_space_separator(
                                                   data_on_date_chosen["Количество выздоровевших"].sum()),
                                               num_dead=format_with_space_separator(
                                                   data_on_date_chosen["Количество умерших"].sum()),
                                               num_infected=format_with_space_separator(data_on_date_chosen[
                                                                                            "Количество оставшихся заболевших"].sum())))

    df_to_graph = data_on_date.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]].sum().reset_index()

    place_all_graphs(df_to_graph)

    loc_info_label.configure(font=font_info)


# Темная тема, изменение графиков
def appear_button_callback():
    global current_window
    if ctk.get_appearance_mode().lower() == "light":
        sns.set_style('darkgrid')
        ctk.set_appearance_mode("dark")
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['figure.facecolor'] = 'black'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['grid.color'] = '#555555'
        plt.rcParams['axes.edgecolor'] = 'white'
        match current_window:
            case "Home":
                home_button_callback()
            case "Calendar":
                cal_button_callback()
            case "Location":
                loc_button_callback()
    else:
        ctk.set_appearance_mode("light")
        sns.reset_defaults()
        plt.rcdefaults()
        sns.set_style('darkgrid')
        match current_window:
            case "Home":
                home_button_callback()
            case "Calendar":
                cal_button_callback()
            case "Location":
                loc_button_callback()
    sa.basic_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]


def option_menu_callback(choice):
    global has_checked
    if not has_checked:
        name_textbox_text.set(sa.loc_main_text + choice + " на " + '%(day)02d.%(month)02d.%(year)d' %
                              {'day': sa.day, 'month': sa.month, 'year': sa.year})
        loc_button_callback()
    else:
        name_textbox_text.set(sa.loc_main_text + choice + " за последние 10 дней")

        data_on_date = pd.DataFrame(
            get_reg_data_db(loc_opt_menu.get(), last_10_writes=True))

        loc_info_text.set(sa.frame_loc_10_text.format(region=loc_opt_menu.get(),
                                                      num_diseased=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество заболевших"].sum() -
                                                          data_on_date.iloc[-1]["Количество заболевших"].sum()),
                                                      num_cured=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество выздоровевших"].sum() -
                                                          data_on_date.iloc[-1]["Количество выздоровевших"].sum()),
                                                      num_dead=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество умерших"].sum() -
                                                          data_on_date.iloc[-1]["Количество умерших"].sum())))

        df_to_graph = data_on_date.groupby(["Дата"])[
            ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]].sum().reset_index()

        place_all_graphs(df_to_graph)

        loc_info_label.configure(font=font_info)


def data_optionmenu_callback(choice):
    year_i = int(year_menu.get())
    month_i = sa.months.index(month_menu.get()) + 1
    first_info = monthrange(year_i, month_i)
    day_f, day_s = 0, 0
    for i in range(0, first_info[0]):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state="disabled", text='')
        # label.unbind()
    for i in range(first_info[0], first_info[1] + first_info[0]):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state=is_day_exist(i - first_info[0] + 1, month_i, year_i), text=str(i - first_info[0] + 1),
                        command=lambda m=i - first_info[0] + 1: date_button_callback(m))
    for i in range(first_info[1] + first_info[0], 42):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state="disabled", text='')


def date_button_callback(choice):
    first_info = monthrange(sa.year, sa.month)
    calendar_frame.grid_slaves(row=2 + (sa.day + first_info[0] - 1) // 7, column=(sa.day + first_info[0] - 1) % 7)[
        0].configure(border_width=0)
    # получает нажатую на календаре кнопку даты и разбирает её, записывает в файл констант
    sa.day = choice
    sa.month = sa.months.index(month_menu.get()) + 1
    sa.year = int(year_menu.get())
    first_info = monthrange(sa.year, sa.month)
    text_tmp = str(name_textbox_text.get())[:-10]
    name_textbox_text.set(text_tmp + '%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.day, 'month': sa.month, 'year': sa.year})
    if (is_in_3):
        loc_button_callback()
    else:
        cal_button_callback()


def last_ten_check_callback():
    global has_checked
    if last_ten_box.get():
        has_checked = True
        calendar_frame.grid_remove()
        text_tmp = str(name_textbox_text.get())[:-10]
        name_textbox_text.set(text_tmp + "последние 10 дней")

        data_on_date = pd.DataFrame(
            get_reg_data_db(loc_opt_menu.get(), last_10_writes=True))

        loc_info_text.set(sa.frame_loc_10_text.format(region=loc_opt_menu.get(),
                                                      num_diseased=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество заболевших"].sum() -
                                                          data_on_date.iloc[-1]["Количество заболевших"].sum()),
                                                      num_cured=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество выздоровевших"].sum() -
                                                          data_on_date.iloc[-1]["Количество выздоровевших"].sum()),
                                                      num_dead=format_with_space_separator(
                                                          data_on_date.iloc[0]["Количество умерших"].sum() -
                                                          data_on_date.iloc[-1]["Количество умерших"].sum())))

        df_to_graph = data_on_date.groupby(["Дата"])[
            ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]].sum().reset_index()

        place_all_graphs(df_to_graph)

        loc_info_label.configure(font=font_info)

    else:
        has_checked = False
        calendar_frame.grid_configure(
            row=2, column=0, padx=(10, 10), pady=(50, 0))
        text_tmp = str(name_textbox_text.get())[:-17]

        loc_button_callback()


# функция устанавливающая конфигурацию новостного блока
def set_news_frame():
    menu_new_val = get_news()  # переменная которая будет хранить полученные новости
    news_frame.grid_columnconfigure(0, weight=1)
    for i, tmp_text in enumerate(menu_new_val):
        label = ctk.CTkTextbox(news_frame,
                               height=120,
                               font=font_news,
                               fg_color=["white", "black"],
                               corner_radius=20,
                               )
        label.insert(ctk.END, tmp_text)
        label.configure(state="disabled")
        label.grid(row=i, column=0, padx=(10, 15), pady=(40, 0), sticky='ew')


# функция устанавливающая конфигурацию календарного блока
def set_calendar_frame():
    calendar_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    year_val = []
    datetime_str = datetime.today().strftime
    for year in range(2019, int(datetime_str("%Y")) + 1):
        year_val.append(str(year))
    for i, name in enumerate(sa.week_name):
        week_label = ctk.CTkLabel(calendar_frame, text=name,
                                  font=font_week, text_color=["black", "white"])
        week_label.grid(row=1, column=i, sticky='ew')

    month_menu.grid(row=0, column=0, columnspan=4, sticky='ew')
    year_menu.grid(row=0, column=4, columnspan=3, sticky='ew')
    for i in range(0, 42):
        button = ctk.CTkButton(calendar_frame, text="",
                               width=20,
                               state="disabled",
                               fg_color="transparent",
                               bg_color="transparent",
                               border_color=["black", "white"],
                               text_color=["black", "white"]
                               )
        button.grid(row=2 + i // 7, column=i % 7)
    sa.day = int(datetime_str("%d"))
    sa.month = int(datetime_str("%m"))
    sa.year = int(datetime_str("%Y"))
    year_menu.configure(values=year_val)
    year_menu.set(year_val[-1])
    month_menu.set(sa.months[int(sa.month) - 1])
    data_optionmenu_callback(-1)


# создание объекта приложения
app = ctk.CTk()
app.title("COVID Now")

# установка базовых размеров окна
app.geometry(initial_geometry)

# определение grid-системы для основного окна
app.grid_rowconfigure((0, 1), weight=1)

app.grid_columnconfigure(2, weight=1)
frame_width = 90

# создание зоны основной навигации
menu_frame = ctk.CTkFrame(master=app, width=90, fg_color=["#D9D9D9", "#4A4A4A"], bg_color=[
    "#D9D9D9", "#4A4A4A"])
# создание зоны для размещения основной информации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color=[
    "white", "black"], bg_color=["white", "black"])
# создание зоны для дашборда/боковых виджетов
info_frame = ctk.CTkFrame(master=app, fg_color=["#D9D9D9", "#4A4A4A"], bg_color=[
    "#D9D9D9", "#4A4A4A"])

# конфигурация расположения зон
menu_frame.grid(row=0, rowspan=3, column=0, sticky="ns")
main_frame.grid(row=0, rowspan=3, column=1, sticky="nsew")
info_frame.grid(row=0, rowspan=3, column=2, sticky="nswe")

# определение grid-системы для зоны размещения основной информации
menu_frame.grid_rowconfigure(3, weight=1)

# определение пути до расположения дополнительных ресурсов
file_path = os.path.dirname(os.path.realpath(__file__))

# установка кастомной фиолетовой темы приложения
ctk.set_default_color_theme(file_path + "\\source\\violet.json")
# загрузка изображений для кнопок навигации - в активном и неактивном состоянии
home_img_a = ctk.CTkImage(light_image=Image.open(file_path + "\\images\\home_w.png"),
                          dark_image=Image.open(
                              file_path + "\\images\\home_b.png"),
                          size=(24, 24))
home_img_d = ctk.CTkImage(light_image=Image.open(file_path + "\images\home_b.png"),
                          dark_image=Image.open(
                              file_path + "\images\home_w.png"),
                          size=(24, 24))

cal_img_a = ctk.CTkImage(light_image=Image.open(file_path + "\images\calendar_w.png"),
                         dark_image=Image.open(
                             file_path + "\images\calendar_b.png"),
                         size=(24, 24))
cal_img_d = ctk.CTkImage(light_image=Image.open(file_path + "\images\calendar_b.png"),
                         dark_image=Image.open(
                             file_path + "\images\calendar_w.png"),
                         size=(24, 24))

loc_img_a = ctk.CTkImage(light_image=Image.open(file_path + "\images\gps_w.png"),
                         dark_image=Image.open(file_path + "\images\gps_b.png"),
                         size=(24, 24))
loc_img_d = ctk.CTkImage(light_image=Image.open(file_path + "\images\gps_b.png"),
                         dark_image=Image.open(file_path + "\images\gps_w.png"),
                         size=(24, 24))

theme_ing = ctk.CTkImage(light_image=Image.open(file_path + "\images\light.png"),
                         dark_image=Image.open(file_path + "\images\moon.png"),
                         size=(24, 24))

# определение кнопок навигации
home_button = ctk.CTkButton(menu_frame,
                            width=90,
                            height=90,
                            text='',
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            text_color=("black", "white"),
                            command=home_button_callback,
                            image=home_img_a
                            )

cal_button = ctk.CTkButton(menu_frame,
                           width=90,
                           height=90,
                           text="",
                           border_width=0,
                           corner_radius=0,
                           border_spacing=0,
                           fg_color='transparent',
                           text_color=("black", "white"),
                           command=cal_button_callback,
                           image=cal_img_d)

loc_button = ctk.CTkButton(menu_frame,
                           width=90,
                           height=90,
                           text="",
                           border_width=0,
                           corner_radius=0,
                           border_spacing=0,
                           fg_color='transparent',
                           text_color=("black", "white"),
                           command=loc_button_callback,
                           image=loc_img_d)

appear_button = ctk.CTkButton(menu_frame,
                              width=90,
                              height=90,
                              text="",
                              border_width=0,
                              corner_radius=0,
                              border_spacing=0,
                              fg_color='transparent',
                              text_color=("black", "white"),
                              command=appear_button_callback,
                              image=theme_ing)

# конфигурация расположения кнопок
home_button.grid(column=0, row=0, sticky="new")
cal_button.grid(column=0, row=1, sticky="new")
loc_button.grid(column=0, row=2, sticky="new")
appear_button.grid(column=0, row=4, sticky="sew")

name_textbox_text = ctk.StringVar()
name_textbox_text.set(
    sa.home_main_text + f"{datetime.today().strftime('%d.%m.%Y')}")

name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent',
                            font=font_label,
                            height=86,
                            textvariable=name_textbox_text,
                            anchor="nw",
                            wraplength=900,
                            justify="left")

# определение grid-системы для окна основной информации и размещение заголовка
main_frame.grid_rowconfigure(2, weight=1)
name_textbox.grid(row=0, column=0, rowspan=1,
                  sticky="new", padx=(54, 0), pady=(33, 0))

# определение и размещение frame-объекта для расположения графиков и инфо-таблички
charts_frame = ctk.CTkFrame(main_frame, fg_color=["white", "black"])
charts_frame.grid(row=1, column=0, rowspan=2, sticky="")

# определение текста и объектов для инфо-табличек, уникальных для каждого экрана
main_info_text = ctk.StringVar()
loc_info_text = ctk.StringVar()
cal_info_text = ctk.StringVar()
main_info_text.set(sa.frame_home_text)
loc_info_text.set(sa.frame_loc_text)
cal_info_text.set(sa.frame_cal_text)
main_info_label = ctk.CTkLabel(charts_frame,
                               width=400,
                               height=250,
                               corner_radius=20,
                               fg_color=["#D9D9D9", "#4A4A4A"],
                               textvariable=main_info_text,
                               wraplength=364,
                               font=font_info,
                               anchor="w",
                               justify="left")
loc_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=loc_info_text,
                              wraplength=364,
                              font=font_info,
                              anchor="w",
                              justify="left")
cal_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=cal_info_text,
                              wraplength=364,
                              font=font_info,
                              anchor="w",
                              justify="left")

# определение frame-объектов для размещения графиков
ill_chart_frame = ctk.CTkFrame(
    charts_frame, width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])
cured_chart_frame = ctk.CTkFrame(
    charts_frame, width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])
death_chart_frame = ctk.CTkFrame(
    charts_frame, width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])

# размещение инфо-табличек
main_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))
loc_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))
cal_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))

# метод tkraise позволяет разместить виджет над всеми остальными, занимающих ту же grid-ячейку
main_info_label.tkraise()

# размещение frame-объектов для графиков

ill_chart_frame.grid(row=0, column=1, pady=(0, 31), padx=(54, 52))
cured_chart_frame.grid(row=1, column=0, pady=(0, 0), padx=(54, 0))
death_chart_frame.grid(row=1, column=1, pady=(0, 0), padx=(54, 52))

# определение объекта для размещения новостей со скроллбаром и его настройка
news_frame = ctk.CTkScrollableFrame(
    info_frame, fg_color=["#D9D9D9", "#4A4A4A"])
set_news_frame()

# определение меню для выбора региона
loc_opt_menu = ctk.CTkOptionMenu(info_frame,
                                 width=225,
                                 height=39,
                                 values=sa.regions,
                                 command=option_menu_callback,
                                 font=font_options)

# определение чекбокса для отключения/включения календаря
last_ten_box = ctk.CTkCheckBox(info_frame,
                               width=225,
                               text="Последние 10 дней",
                               font=font_checkbox,
                               command=last_ten_check_callback)

# определение frame-объекта для размещения виджета календаря
calendar_frame = ctk.CTkFrame(master=info_frame, fg_color=[
    "white", "black"], width=255)

# создание элементов календаря, отвечающих за месяц и год

month_menu = ctk.CTkOptionMenu(calendar_frame, values=sa.months,
                               font=font_month,
                               corner_radius=0,
                               width=120,
                               command=data_optionmenu_callback)
year_menu = ctk.CTkOptionMenu(calendar_frame,
                              values=[],
                              font=font_year,
                              corner_radius=0,
                              width=90,
                              command=data_optionmenu_callback)
set_calendar_frame()

# симуляция нажатия на домашнюю кнопку для установки первого экрана перед запуском
home_button_callback()
# запуск основного цикла программы
perform_check(ctk)
app.mainloop()
