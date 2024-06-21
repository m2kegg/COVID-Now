import os
from calendar import monthrange
from datetime import datetime

import customtkinter as ctk
from PIL import Image
import pandas as pd
import seaborn as sns
import tkinter as tk

import samples as sa
import scrap_stats
import form_diagrams
import misc
import config


data_today = pd.DataFrame(scrap_stats.get_today_data_db())
data_all = pd.DataFrame(scrap_stats.get_all_data_db(scrap_stats.date.today()))

# Проверка на нахождение в location-окне
IS_IN_3 = False

# Проверка на выделение чекбокса
HAS_CHECKED = False

# Окно в данный момент
CURRENT_WINDOW = ""

form_diagrams.sns.set_style('darkgrid')

# Расстановка графиков по фреймам
def place_all_graphs(df_to_graph):
    misc.clear_frame(ill_chart_frame)
    misc.clear_frame(death_chart_frame)
    misc.clear_frame(cured_chart_frame)

    form_diagrams.create_and_place_graph(df_to_graph[["Дата", "Количество заболевших"]],
    "Количество заболевших", ill_chart_frame,
                           "red")
    form_diagrams.create_and_place_graph(df_to_graph[["Дата", "Количество умерших"]],
    "Количество умерших", death_chart_frame,
                           "blue")
    form_diagrams.create_and_place_graph(df_to_graph[["Дата", "Количество выздоровевших"]],
    "Количество выздоровевших",
                        cured_chart_frame, "green")


def home_button_callback():
    global CURRENT_WINDOW
    CURRENT_WINDOW = "Home"

    home_button.configure(fg_color=ctk.ThemeManager.\
                          theme["CTkButton"]["fg_color"], image=home_img_a)
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
    show_periond_box.deselect()
    period_frame.grid_remove()
    name_textbox_text.set(sa.HOME_MAIN_TEXT
                          + f"{misc.datetime.today().strftime('%d.%m.%Y')}")
    main_info_text.set(sa.FRAME_MAIN_TEXT.\
                       format(date_last_call=str(datetime.today().strftime('%d.%m.%y')),
                              num_diseased=misc.format_with_space_separator(data_today["Количество заболевших"].sum()),
                              num_cured=misc.format_with_space_separator(data_today["Количество выздоровевших"].sum()),
                              num_dead=misc.format_with_space_separator(data_today["Количество умерших"].sum()),
                              num_infected=misc.format_with_space_separator(data_today["Количество оставшихся заболевших"].sum())))
    main_info_label.configure(font=config.FONT_INFO)

    df_to_graph = data_all.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]]\
        .sum().reset_index()

    place_all_graphs(df_to_graph)


def cal_button_callback():
    global IS_IN_3, CURRENT_WINDOW
    IS_IN_3 = False
    CURRENT_WINDOW = "Calendar"
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
    show_periond_box.grid_remove()
    show_periond_box.deselect()
    period_frame.grid_remove()
    calendar_frame.grid_configure(
        row=0, column=0, padx=(10, 10), pady=(50, 0), sticky="new")

    filter_date = misc.datetime(sa.YEAR, sa.MONTH, sa.DAY)

    if filter_date.weekday() != 1 and filter_date >= misc.datetime(2023, 5, 16):
        day_of_week = filter_date.weekday()

        if day_of_week > 1:
            days_to_tuesday = day_of_week - 1
        else:
            days_to_tuesday = 6

        prev_tuesday = filter_date - scrap_stats.timedelta(days=days_to_tuesday)
        filter_date = prev_tuesday
        sa.DAY = prev_tuesday.day
        sa.MONTH = prev_tuesday.month
        sa.YEAR = prev_tuesday.year

    name_textbox_text.set(sa.CAL_MAIN_TEXT + '%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})

    data_on_date_all = pd.DataFrame(scrap_stats.get_all_data_db
                                    (misc.datetime(sa.YEAR, sa.MONTH, sa.DAY)))
    data_on_date_all['Дата'] = pd.to_datetime(data_on_date_all['Дата'])
    data_on_date = data_on_date_all[data_on_date_all['Дата']
                                    == filter_date]

    cal_info_text.set(sa.FRAME_CAL_TEXT.\
                      format(date_last_call=misc.\
                             datetime(sa.YEAR, sa.MONTH, sa.DAY).strftime('%d.%m.%y'),
                             num_diseased=misc.format_with_space_separator(
                                 data_on_date["Количество заболевших"].sum()),
                             num_cured=misc.format_with_space_separator(
                                 data_on_date["Количество выздоровевших"].sum()),
                             num_dead=misc.format_with_space_separator(
                                 data_on_date["Количество умерших"].sum()),
                             num_infected=misc.format_with_space_separator(
                                 data_on_date["Количество оставшихся заболевших"].sum())))

    df_to_graph = data_on_date_all.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]]\
        .sum().reset_index()

    place_all_graphs(df_to_graph)


def loc_button_callback():
    global IS_IN_3, CURRENT_WINDOW
    IS_IN_3 = True
    CURRENT_WINDOW = "Location"
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(
        fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], image=loc_img_a)

    info_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    loc_info_label.tkraise()

    news_frame.grid_remove()

    loc_opt_menu.grid_configure(row=0, column=0, padx=(
        13, 13), pady=(33, 0), sticky="ew")
    last_ten_box.grid_configure(
        row=1, column=0, padx=(13, 13), pady=(40, 0), sticky="")
    show_periond_box.grid_configure(
        row=2, column=0, padx=(13, 13), pady=(40, 0), sticky="")
    calendar_frame.grid_configure(
        row=3, column=0, padx=(10, 10), pady=(50, 0), sticky="new")

    last_ten_box.deselect()
    last_ten_box.configure(command=last_ten_check_callback)

    name_textbox_text.set(sa.LOC_MAIN_TEXT + loc_opt_menu.get() + " на " +
            '%(day)02d.%(month)02d.%(year)d' % {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})

    data_on_date = pd.DataFrame(
        scrap_stats.get_reg_data_db(loc_opt_menu.get(),
        date_chosen=misc.datetime(sa.YEAR, sa.MONTH, sa.DAY)))

    data_on_date_chosen = data_on_date.iloc[0]
    loc_info_text.set(sa.FRAME_LOC_TEXT.\
                      format(date_last_call=misc.\
                            datetime(sa.YEAR, sa.MONTH, sa.DAY).strftime('%d.%m.%y'),
                            region=loc_opt_menu.get(),
                            num_diseased=misc.format_with_space_separator(
                                data_on_date_chosen["Количество заболевших"].sum()),
                            num_cured=misc.format_with_space_separator(
                                data_on_date_chosen["Количество выздоровевших"].sum()),
                            num_dead=misc.format_with_space_separator(
                                data_on_date_chosen["Количество умерших"].sum()),
                            num_infected=misc.format_with_space_separator(
                                data_on_date_chosen["Количество оставшихся заболевших"].sum())))

    df_to_graph = data_on_date.groupby(["Дата"])[
        ["Количество заболевших", "Количество умерших",
         "Количество выздоровевших"]].sum().reset_index()

    place_all_graphs(df_to_graph)

    loc_info_label.configure(font=config.FONT_INFO)


# Темная тема, изменение графиков
def appear_button_callback():
    global CURRENT_WINDOW
    if ctk.get_appearance_mode().lower() == "light":
        form_diagrams.sns.set_style('darkgrid')
        ctk.set_appearance_mode("dark")
        form_diagrams.plt.rcParams['axes.facecolor'] = 'black'
        form_diagrams.plt.rcParams['figure.facecolor'] = 'black'
        form_diagrams.plt.rcParams['text.color'] = 'white'
        form_diagrams.plt.rcParams['axes.labelcolor'] = 'white'
        form_diagrams.plt.rcParams['xtick.color'] = 'white'
        form_diagrams.plt.rcParams['ytick.color'] = 'white'
        form_diagrams.plt.rcParams['grid.color'] = '#555555'
        form_diagrams.plt.rcParams['axes.edgecolor'] = 'white'
        if CURRENT_WINDOW == "Home":
            home_button_callback()
        elif CURRENT_WINDOW == "Calendar":
            cal_button_callback()
        else:
            loc_button_callback()
    else:
        ctk.set_appearance_mode("light")
        form_diagrams.sns.reset_defaults()
        form_diagrams.plt.rcdefaults()
        form_diagrams.sns.set_style('darkgrid')
        if CURRENT_WINDOW == "Home":
            home_button_callback()
        elif CURRENT_WINDOW == "Calendar":
            cal_button_callback()
        else:
            loc_button_callback()
    sa.BASIC_COLOR = ctk.ThemeManager.theme["CTkButton"]["fg_color"]


def option_menu_callback(choice):
    global HAS_CHECKED
    if not HAS_CHECKED:
        if show_periond_box.get():
            name_textbox_text.set(sa.LOC_MAIN_TEXT + choice
                                  + " на " + '%(day)02d.%(month)02d.%(year)d' %
                                  {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})
            loc_button_callback()
            calendar_frame.grid_remove()
        else:
            name_textbox_text.set(sa.LOC_MAIN_TEXT + choice
                                  + " на " + '%(day)02d.%(month)02d.%(year)d' %
                                  {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})
            loc_button_callback()
    else:
        name_textbox_text.set(sa.LOC_MAIN_TEXT + choice + " за последние 10 дней")

        data_on_date = pd.DataFrame(
            scrap_stats.get_reg_data_db(loc_opt_menu.get(), last_10_writes=True))

        loc_info_text.set(sa.FRAME_LOC_10_TEXT.\
                          format(region=loc_opt_menu.get(),
                                 num_diseased=misc.format_with_space_separator(
                                     data_on_date.iloc[0]["Количество заболевших"].sum() -
                                     data_on_date.iloc[-1]["Количество заболевших"].sum()),
                                 num_cured=misc.format_with_space_separator(
                                     data_on_date.iloc[0]["Количество выздоровевших"].sum() -
                                     data_on_date.iloc[-1]["Количество выздоровевших"].sum()),
                                 num_dead=misc.format_with_space_separator(
                                     data_on_date.iloc[0]["Количество умерших"].sum() -
                                     data_on_date.iloc[-1]["Количество умерших"].sum())))

        df_to_graph = data_on_date.groupby(["Дата"])[
            ["Количество заболевших", "Количество умерших",
             "Количество выздоровевших"]].sum().reset_index()

        place_all_graphs(df_to_graph)

        loc_info_label.configure(font=config.FONT_INFO)


def data_optionmenu_callback(choice):
    year_i = int(year_menu.get())
    month_i = sa.MONTHS.index(month_menu.get()) + 1
    first_info = monthrange(year_i, month_i)
    for i in range(0, first_info[0]):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state="disabled", text='')
    for i in range(first_info[0], first_info[1] + first_info[0]):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state=misc.is_day_exist(i - first_info[0] + 1, month_i, year_i),
                        text=str(i - first_info[0] + 1),
                        command=lambda m=i - first_info[0] + 1: date_button_callback(m))
    for i in range(first_info[1] + first_info[0], 42):
        label = calendar_frame.grid_slaves(row=2 + i // 7, column=i % 7)[0]
        label.configure(state="disabled", text='')


def date_button_callback(choice):
    first_info = monthrange(sa.YEAR, sa.MONTH)
    calendar_frame.grid_slaves(row=2 + (sa.DAY + first_info[0] - 1) // 7,
                               column=(sa.DAY + first_info[0] - 1) % 7)[
                               0].configure(border_width=0)
    # получает нажатую на календаре кнопку даты и разбирает её, записывает в файл констант
    sa.DAY = choice
    sa.MONTH = sa.MONTHS.index(month_menu.get()) + 1
    sa.YEAR = int(year_menu.get())
    first_info = monthrange(sa.YEAR, sa.MONTH)
    text_tmp = str(name_textbox_text.get())[:-10]
    calendar_frame.grid_slaves(row=2 + (sa.DAY + first_info[0] - 1) // 7, column=(sa.DAY + first_info[
        0] - 1) % 7)[0].configure(border_width=1)
    name_textbox_text.set(text_tmp + '%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})
    if IS_IN_3:
        loc_button_callback()
    else:
        cal_button_callback()


def last_ten_check_callback():
    global HAS_CHECKED
    if last_ten_box.get():
        HAS_CHECKED = True
        calendar_frame.grid_remove()
        period_frame.grid_remove()
        # действуем в зависимости от того, был ли выбран другой чекбокс
        if (show_periond_box.get()):
            text_tmp = str(name_textbox_text.get())
            if text_tmp[len(text_tmp) - 1] == ']':  # если в тексте был диапазон
                text_tmp = text_tmp[:-24]
        else:
            text_tmp = str(name_textbox_text.get())[:-10]
        name_textbox_text.set(text_tmp + "последние 10 дней")
        show_periond_box.deselect()  # отменяем выбор другого чекбокса

        data_on_date = pd.DataFrame(
            scrap_stats.get_reg_data_db(loc_opt_menu.get(), last_10_writes=True))

        loc_info_text.set(sa.FRAME_LOC_10_TEXT.\
                          format(region=loc_opt_menu.get(),
                                 num_diseased=misc.format_with_space_separator(
                                      data_on_date.iloc[0]["Количество заболевших"].sum() -
                                      data_on_date.iloc[-1]["Количество заболевших"].sum()),
                                 num_cured=misc.format_with_space_separator(
                                      data_on_date.iloc[0]["Количество выздоровевших"].sum() -
                                      data_on_date.iloc[-1]["Количество выздоровевших"].sum()),
                                 num_dead=misc.format_with_space_separator(
                                      data_on_date.iloc[0]["Количество умерших"].sum() -
                                      data_on_date.iloc[-1]["Количество умерших"].sum())))

        df_to_graph = data_on_date.groupby(["Дата"])[
            ["Количество заболевших", "Количество умерших", "Количество выздоровевших"]]\
            .sum().reset_index()

        place_all_graphs(df_to_graph)

        loc_info_label.configure(font=config.FONT_INFO)

    else:
        HAS_CHECKED = False
        calendar_frame.grid_configure(
            row=3, column=0, padx=(10, 10), pady=(50, 0))
        text_tmp = str(name_textbox_text.get())[:-17]
        name_textbox_text.set(text_tmp + '%(day)02d.%(month)02d.%(year)d' %
                              {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})

        loc_button_callback()

def show_period_ckeck_callback():
    if show_periond_box.get():
        text_tmp = ''
        calendar_frame.grid_remove()
        # действуем в зависимости от того, был ли активен другой чекбокс
        if last_ten_box.get():
            text_tmp = str(name_textbox_text.get())[:-17]
        else:
            text_tmp = str(name_textbox_text.get())[:-10]
        last_ten_box.deselect()  # отменяем выделение другого чекбокса
        name_textbox_text.set(text_tmp)

        period_frame.grid_configure(row=3, column=0, padx=(
            10, 10), pady=(50, 0), sticky='ew')
    else:
        period_frame.grid_remove()
        text_tmp = str(name_textbox_text.get())
        # если в тексте поля был диапазон, стираем его
        if text_tmp[len(text_tmp)-1] == ']':
            text_tmp = text_tmp[:-24]
        name_textbox_text.set(text_tmp+'%(day)02d.%(month)02d.%(year)d' %
                              {'day': sa.DAY, 'month': sa.MONTH, 'year': sa.YEAR})
        calendar_frame.grid_configure(
            row=3, column=0, padx=(10, 10), pady=(50, 0), sticky='ew')


def period_button_callback():
    year_1 = int(period_frame.grid_slaves(row=1, column=0)[0].get())
    month_1 = sa.MONTHS.index(
        period_frame.grid_slaves(row=1, column=1)[0].get())+1

    year_2 = int(period_frame.grid_slaves(row=3, column=0)[0].get())
    month_2 = sa.MONTHS.index(
        period_frame.grid_slaves(row=3, column=1)[0].get())+1

    day_1 = (period_frame.grid_slaves(row=1, column=2)[0].get())
    day_2 = (period_frame.grid_slaves(row=3, column=2)[0].get())

    # проверяем корректность 1 дня
    flag_1 = check_entry_day(day_1, month_1, year_1)
    # проверяем корректность 2 дня
    flag_2 = check_entry_day(day_2, month_2, year_2)

    day_fir = datetime(year_1, month_1, int(day_1))
    day_sec = datetime(year_2, month_2, int(day_2))

    #если оба дня корректны и они правильно расположены
    if flag_1 and flag_2 and datetime(year_1, month_1, int(day_1)) < datetime(year_2, month_2, int(day_2)):
        day_1 = int(day_1)
        day_2 = int(day_2)

        data = scrap_stats.get_two_dates_db(loc_opt_menu.get(), day_fir, day_sec)

        df_reg = pd.DataFrame(data)

        place_all_graphs(df_reg)

        text_tmp = str(name_textbox_text.get())
        if text_tmp[len(text_tmp)-1] == ']':
            text_tmp = text_tmp[:-24]
        name_textbox_text.set(text_tmp +
                              '[%(d1)02d.%(m1)02d.%(y1)d, %(d2)02d.%(m2)02d.%(y2)d]'
                              % {'d1': day_1, 'm1': month_1, 'y1': year_1,
                                 'd2': day_2, 'm2': month_2, 'y2': year_2})

        loc_info_text.set(sa.PERIOD_MAIN_TEXT.format(
            date_first=day_fir.strftime('%d.%m.%Y'),
            date_last=day_sec.strftime('%d.%m.%Y'),
            region=loc_opt_menu.get(),
            num_diseased=misc.format_with_space_separator(df_reg.iloc[-1]["Количество заболевших"].sum() -
                         df_reg.iloc[0]["Количество заболевших"].sum()),
            num_cured=misc.format_with_space_separator(df_reg.iloc[-1]["Количество выздоровевших"].sum() -
                         df_reg.iloc[0]["Количество выздоровевших"].sum()),
            num_dead=misc.format_with_space_separator(df_reg.iloc[-1]["Количество умерших"].sum() -
                         df_reg.iloc[0]["Количество умерших"].sum()
        )
        ))
        #
        # отклик на полученный период
        #
    else:
        button = period_frame.grid_slaves(row=4, column=0)[0]
        button.configure(text='Неправильные данные')
        # без нарушения главного цикла, надпись на кнопке будет изменена на 4 секунды
        button.after(4000, lambda: button.configure(text='Найти данные'))


def validation_command(input):
    # команда валидации маски ввода
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


# функция устанавливающая конфигурацию новостного блока
def set_news_frame():
    menu_new_val = scrap_stats.get_news()  # переменная которая будет хранить полученные новости
    news_frame.grid_columnconfigure(0, weight=1)
    for i, tmp_text in enumerate(menu_new_val):
        label = ctk.CTkTextbox(news_frame,
                               height=120,
                               font=config.FONT_NEWS,
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
    datetime_str = misc.datetime.today().strftime
    for year in range(2019, int(datetime_str("%Y")) + 1):
        year_val.append(str(year))
    for i, name in enumerate(sa.WEEK_NAME):
        week_label = ctk.CTkLabel(calendar_frame, text=name,
                                  font=config.FONT_WEEK, text_color=["black", "white"])
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
    sa.DAY = int(datetime_str("%d"))
    sa.MONTH = int(datetime_str("%m"))
    sa.YEAR = int(datetime_str("%Y"))
    year_menu.configure(values=year_val)
    year_menu.set(year_val[-1])
    month_menu.set(sa.MONTHS[int(sa.MONTH) - 1])
    data_optionmenu_callback(-1)

def set_period_frame():
    reg = app.register(validation_command)  # создание команды для маски ввода
    period_frame.grid_rowconfigure(0, weight=1)
    period_frame.grid_columnconfigure((0, 1, 2), weight=1)

    label_first = ctk.CTkLabel(period_frame,
                               text="Первая дата",
                               font=("Roboto", 16),
                               text_color=["black", "white"],
                               anchor="nw",
                               justify='left'
                               )
    label_second = ctk.CTkLabel(period_frame,
                                text="Вторая дата",
                                font=("Roboto", 16),
                                text_color=["black", "white"],
                                anchor="nw",
                                justify='left')
    # устанавливаем тот же список что и у календаря
    year_value = year_menu.cget("values")
    year_1 = ctk.CTkOptionMenu(
        period_frame, width=60, values=year_value, corner_radius=5)
    month_1 = ctk.CTkOptionMenu(
        period_frame, width=60, values=sa.MONTHS, corner_radius=5)
    year_1.set(year_value[-1])  # устанавливаем дефолтные значения
    month_1.set(sa.MONTHS[int(sa.MONTH)-1])

    year_2 = ctk.CTkOptionMenu(
        period_frame, width=60, values=year_value, corner_radius=5)
    month_2 = ctk.CTkOptionMenu(
        period_frame, width=60, values=sa.MONTHS, corner_radius=5)
    year_2.set(year_value[-1])
    month_2.set(sa.MONTHS[int(sa.MONTH)-1])

    # дни вводятся через поля с маской ввода
    day_e_1 = ctk.CTkEntry(period_frame, width=50, validate="key",
                           validatecommand=(reg, '%P'), corner_radius=5)
    day_e_2 = ctk.CTkEntry(period_frame, width=50, validate="key",
                           validatecommand=(reg, '%P'), corner_radius=5)

    label_first.grid(row=0, column=0, columnspan=3,
                     sticky="ew", pady=(15, 5), padx=10)
    label_second.grid(row=2, column=0, columnspan=3,
                      sticky="ew", pady=(5, 5), padx=10)
    year_1.grid(row=1, column=0, pady=(0, 10), padx=(10, 5), sticky="ew")
    month_1.grid(row=1, column=1, pady=(0, 10), sticky="ew")
    day_e_1.grid(row=1, column=2, pady=(0, 10), padx=(5, 10), sticky="ew")

    year_2.grid(row=3, column=0, pady=(0, 10), padx=(10, 5), sticky="ew")
    month_2.grid(row=3, column=1, pady=(0, 10), sticky="ew")
    day_e_2.grid(row=3, column=2, pady=(0, 10), padx=(5, 10), sticky="ew")

    # устанавливаем дефолтные значения
    day_e_1.insert(ctk.END, sa.DAY)
    day_e_2.insert(ctk.END, sa.DAY)
    # кнопка для вычислений
    period_button = ctk.CTkButton(
        period_frame, text='Найти данные', command=period_button_callback)
    period_button.grid(row=4, column=0, columnspan=3,
                       padx=(10, 10), pady=(0, 10), sticky="ew")

def check_entry_day(day: str, month: int, year: int):
    # функция проверяет корректен ли день в поле ввода
    if day == "":
        return False
    day_i = int(day)
    if day_i > monthrange(year, month)[1]:
        return False
    if day_i < 1:
        return False
    if datetime(year, month, day_i) > datetime.today():
        return False
    return True


# создание объекта приложения
app = ctk.CTk()
app.title("COVID Now")

# установка базовых размеров окна
app.geometry(config.INITIAL_GEOMETRY)

# определение grid-системы для основного окна
app.grid_rowconfigure((0, 1), weight=1)

app.grid_columnconfigure(2, weight=1)
FRAME_WIDTH = 90

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
ctk.set_default_color_theme("source/violet.json")
# загрузка изображений для кнопок навигации - в активном и неактивном состоянии
home_img_a = ctk.CTkImage(light_image=Image.open("images/home_w.png"),
                          dark_image=Image.open(
                              "images/home_b.png"),
                          size=(24, 24))
home_img_d = ctk.CTkImage(light_image=Image.open("images/home_b.png"),
                          dark_image=Image.open(
                              "images/home_w.png"),
                          size=(24, 24))

cal_img_a = ctk.CTkImage(light_image=Image.open("images/calendar_w.png"),
                         dark_image=Image.open(
                             "images/calendar_b.png"),
                         size=(24, 24))
cal_img_d = ctk.CTkImage(light_image=Image.open("images/calendar_b.png"),
                         dark_image=Image.open(
                             "images/calendar_w.png"),
                         size=(24, 24))

loc_img_a = ctk.CTkImage(light_image=Image.open("images/gps_w.png"),
                         dark_image=Image.open("images/gps_b.png"),
                         size=(24, 24))
loc_img_d = ctk.CTkImage(light_image=Image.open("images/gps_b.png"),
                         dark_image=Image.open("images/gps_w.png"),
                         size=(24, 24))

theme_ing = ctk.CTkImage(light_image=Image.open("images/light.png"),
                         dark_image=Image.open("images/moon.png"),
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
    sa.HOME_MAIN_TEXT + f"{misc.datetime.today().strftime('%d.%m.%Y')}")

name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent',
                            font=config.FONT_LABEL,
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
main_info_text.set(sa.FRAME_MAIN_TEXT)
loc_info_text.set(sa.FRAME_LOC_TEXT)
cal_info_text.set(sa.FRAME_CAL_TEXT)
main_info_label = ctk.CTkLabel(charts_frame,
                               width=400,
                               height=250,
                               corner_radius=20,
                               fg_color=["#D9D9D9", "#4A4A4A"],
                               textvariable=main_info_text,
                               wraplength=364,
                               font=config.FONT_INFO,
                               anchor="w",
                               justify="left")
loc_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=loc_info_text,
                              wraplength=364,
                              font=config.FONT_INFO,
                              anchor="w",
                              justify="left")
cal_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=cal_info_text,
                              wraplength=364,
                              font=config.FONT_INFO,
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
                                 values=sa.REGIONS,
                                 command=option_menu_callback,
                                 font=config.FONT_OPTIONS)

# определение чекбокса для отключения/включения календаря
last_ten_box = ctk.CTkCheckBox(info_frame,
                               width=225,
                               text="Последние 10 дней",
                               font=config.FONT_CHECKBOX,
                               command=last_ten_check_callback)

# определение frame-объекта для размещения виджета календаря
calendar_frame = ctk.CTkFrame(master=info_frame, fg_color=[
    "white", "black"], width=255)

# создание элементов календаря, отвечающих за месяц и год

month_menu = ctk.CTkOptionMenu(calendar_frame, values=sa.MONTHS,
                               font=config.FONT_MONTH,
                               corner_radius=0,
                               width=120,
                               command=data_optionmenu_callback)
year_menu = ctk.CTkOptionMenu(calendar_frame,
                              values=[],
                              font=config.FONT_YEAR,
                              corner_radius=0,
                              width=90,
                              command=data_optionmenu_callback)
# создание меню выбора периода
show_periond_box = ctk.CTkCheckBox(info_frame,
                                   width=225,
                                   text="Указать период",
                                   font=("Roboto", 16),
                                   command=show_period_ckeck_callback)

period_frame = ctk.CTkFrame(master=info_frame, fg_color=[
                            "white", "black"], width=255, height=525,)


set_calendar_frame()
set_period_frame()
home_button_callback()
scrap_stats.perform_check(ctk)
app.mainloop()
