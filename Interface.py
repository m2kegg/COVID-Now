import customtkinter as ctk
from PIL import Image
from datetime import datetime
import samples as sa
import os
from calendar import monthrange
import tkinter as tk

# Про конфигурацию текста в прямоугольниках - теперь для каждого экрана есть свой собственный Label-объект
# с настроенной переменной. main_info_label -> main_info_text. При помощи метода .set для text переменных
# можно динамически менять содержание текста label без метода configure.


def home_button_callback():
    home_button.configure(fg_color=sa.basic_color, image=home_img_a)
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
    show_periond_box.grid_remove()
    calendar_frame.grid_remove()

    name_textbox_text.set(
        sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")
    main_info_label.configure(text=sa.frame_home_text)


def cal_button_callback():
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color=sa.basic_color, image=cal_img_a)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0, 1, 2), weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    cal_info_label.tkraise()

    news_frame.grid_remove()
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    show_periond_box.grid_remove()
    calendar_frame.grid_configure(
        row=0, column=0, padx=(10, 10), pady=(50, 0), sticky="new")

    name_textbox_text.set(sa.cal_main_text+'%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.day, 'month': sa.month, 'year': sa.year})
    main_info_label.configure(text=sa.frame_cal_text)


def loc_button_callback():
    sa.frame_loc_text = "WORKED"
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color=sa.basic_color, image=loc_img_a)

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
    name_textbox_text.set(sa.loc_main_text+loc_opt_menu.get()+" на " +
                          '%(day)02d.%(month)02d.%(year)d' % {'day': sa.day, 'month': sa.month, 'year': sa.year})
    main_info_label.configure(text=sa.frame_loc_text)


def appear_button_callback():
    if ctk.get_appearance_mode().lower() == "light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")
    sa.basic_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]


def option_menu_callback(choice):
    name_textbox_text.set(sa.loc_main_text+choice+" на "+'%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.day, 'month': sa.month, 'year': sa.year})


def data_optionmenu_callback(choice):

    year_i = int(year_menu.get())
    month_i = sa.months.index(month_menu.get())+1
    first_info = monthrange(year_i, month_i)
    day_f, day_s = 0, 0
    for i in range(0, first_info[0]):
        label = calendar_frame.grid_slaves(row=2+i//7, column=i % 7)[0]
        label.configure(state="disabled", text='')

    for i in range(first_info[0], first_info[1]+first_info[0]):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i % 7)[0]
        button.configure(state=is_day_exist(i-first_info[0]+1, month_i, year_i), text=str(i-first_info[0]+1),
                         command=lambda m=i-first_info[0]+1: date_button_callback(m))

        # command=lambda m=i-first_info[0]+1:date_button_callback(m )

    for i in range(first_info[1]+first_info[0], 42):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i % 7)[0]
        button.configure(state="disabled", text='')
    # if (choice != -1):
    #    date_button_callback(1)
    # else:
    #    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(sa.day+first_info[0]-1)%7)[0].configure(border_width=1)


def date_button_callback(choice):
    first_info = monthrange(sa.year, sa.month)
    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(
        sa.day+first_info[0]-1) % 7)[0].configure(border_width=0)
    # получает нажатую на календаре кнопку даты и разбирает её, записывает в файл констант
    sa.day = choice
    sa.month = sa.months.index(month_menu.get())+1
    sa.year = int(year_menu.get())
    first_info = monthrange(sa.year, sa.month)
    text_tmp = str(name_textbox_text.get())[:-10]
    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(
        sa.day+first_info[0]-1) % 7)[0].configure(border_width=1)
    name_textbox_text.set(text_tmp+'%(day)02d.%(month)02d.%(year)d' %
                          {'day': sa.day, 'month': sa.month, 'year': sa.year})


def last_ten_check_callback():
    if last_ten_box.get():
        calendar_frame.grid_remove()
        period_frame.grid_remove()
        # действуем в зависимости от того, был ли выбран другой чекбокс
        if (show_periond_box.get()):
            text_tmp = str(name_textbox_text.get())
            if text_tmp[len(text_tmp)-1] == ']':  # если в тексте был диапазон
                text_tmp = text_tmp[:-24]
        else:
            text_tmp = str(name_textbox_text.get())[:-10]
        name_textbox_text.set(text_tmp+"последние 10 дней")
        show_periond_box.deselect()  # отменяем выбор другого чекбокса
    else:
        calendar_frame.grid_configure(
            row=3, column=0, padx=(10, 10), pady=(50, 0))
        text_tmp = str(name_textbox_text.get())[:-17]
        name_textbox_text.set(text_tmp+'%(day)02d.%(month)02d.%(year)d' %
                              {'day': sa.day, 'month': sa.month, 'year': sa.year})


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
                              {'day': sa.day, 'month': sa.month, 'year': sa.year})
        calendar_frame.grid_configure(
            row=3, column=0, padx=(10, 10), pady=(50, 0), sticky='ew')


def period_button_callback():
    year_1 = int(period_frame.grid_slaves(row=1, column=0)[0].get())
    month_1 = sa.months.index(
        period_frame.grid_slaves(row=1, column=1)[0].get())+1

    year_2 = int(period_frame.grid_slaves(row=3, column=0)[0].get())
    month_2 = sa.months.index(
        period_frame.grid_slaves(row=3, column=1)[0].get())+1

    day_1 = (period_frame.grid_slaves(row=1, column=2)[0].get())
    day_2 = (period_frame.grid_slaves(row=3, column=2)[0].get())

    # проверяем корректность 1 дня
    flag_1 = check_entry_day(day_1, month_1, year_1)
    # проверяем корректность 2 дня
    flag_2 = check_entry_day(day_2, month_2, year_2)

    #если оба дня корректны и они правильно расположены 
    if flag_1 and flag_2 and datetime(year_1, month_1, int(day_1)) < datetime(year_2, month_2, int(day_2)):
        day_1 = int(day_1)
        day_2 = int(day_2)
        text_tmp = str(name_textbox_text.get())
        if text_tmp[len(text_tmp)-1] == ']':
            text_tmp = text_tmp[:-24]
        name_textbox_text.set(text_tmp +
                              '[%(d1)02d.%(m1)02d.%(y1)d, %(d2)02d.%(m2)02d.%(y2)d]'
                              % {'d1': day_1, 'm1': month_1, 'y1': year_1,
                                 'd2': day_2, 'm2': month_2, 'y2': year_2})
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


def set_news_frame():
    menu_new_val = ["https://www.yandex.ru/search/?text=ctk+textbox+for+links&lr=213",
                    "Вакцина «Спутник» от коронавируса для подростков может поступить в оборот через два месяца"]  # переменная которая будет хранить полученные новости
    news_frame.grid_columnconfigure(0, weight=1)
    for i, tmp_text in enumerate(menu_new_val):
        label = ctk.CTkTextbox(news_frame,
                               height=120,

                               font=("Roboto Mono", 13),
                               fg_color=["white", "black"],
                               corner_radius=20,
                               )
        label.insert(ctk.END, tmp_text)
        label.configure(state="disabled")
        label.grid(row=i, column=0, padx=(10, 15), pady=(40, 0), sticky='ew')


def set_calendar_frame():
    calendar_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    year_val = []
    datetime_str = datetime.today().strftime
    for year in range(2020, int(datetime_str("%Y"))+1):
        year_val.append(str(year))
    for i, name in enumerate(sa.week_name):
        week_label = ctk.CTkLabel(calendar_frame, text=name, font=(
            "Roboto", 12), text_color=["black", "white"])
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
        button.grid(row=2+i//7, column=i % 7)
    sa.day = int(datetime_str("%d"))
    sa.month = int(datetime_str("%m"))
    sa.year = int(datetime_str("%Y"))
    year_menu.configure(values=year_val)
    year_menu.set(year_val[-1])
    month_menu.set(sa.months[int(sa.month)-1])
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
        period_frame, width=60, values=sa.months, corner_radius=5)
    year_1.set(year_value[-1])  # устанавливаем дефолтные значения
    month_1.set(sa.months[int(sa.month)-1])

    year_2 = ctk.CTkOptionMenu(
        period_frame, width=60, values=year_value, corner_radius=5)
    month_2 = ctk.CTkOptionMenu(
        period_frame, width=60, values=sa.months, corner_radius=5)
    year_2.set(year_value[-1])
    month_2.set(sa.months[int(sa.month)-1])

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
    day_e_1.insert(ctk.END, sa.day)
    day_e_2.insert(ctk.END, sa.day)
    # кнопка для вычислений
    period_button = ctk.CTkButton(
        period_frame, text='Найти данные', command=period_button_callback)
    period_button.grid(row=4, column=0, columnspan=3,
                       padx=(10, 10), pady=(0, 10), sticky="ew")


def is_day_exist(day: int, month: int, year: int):

    now_date = datetime(year, month, day)
    if now_date < datetime(2020, 3, 27) or now_date > datetime.today():
        return "disabled"
    if now_date <= datetime(2023, 5, 15):
        return "normal"
    if now_date > datetime(2023, 5, 16) and now_date.weekday() == 1:
        return "normal"

    return "disabled"  # функция определяющая имеет ли день статистику или нет, требует доработки


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


app = ctk.CTk()
app.title("COVID Now")
app.geometry("1280x720")  # временное решение создания размера окна

app.grid_rowconfigure((0, 1), weight=1)  # определение grid-системы
app.grid_columnconfigure(2, weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color=["#D9D9D9", "#4A4A4A"], bg_color=[
                          "#D9D9D9", "#4A4A4A"])  # создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color=[
                          "white", "black"], bg_color=["white", "black"])  # создание основной зоны
info_frame = ctk.CTkFrame(master=app, fg_color=["#D9D9D9", "#4A4A4A"], bg_color=[
                          "#D9D9D9", "#4A4A4A"])  # создание зоны новостей

# расположение зоны основной навигации
menu_frame.grid(row=0, rowspan=3, column=0, sticky="ns")
main_frame.grid(row=0, rowspan=3, column=1, sticky="nsew")
# инфо-режим стоит по умолчанию при запуске программы
info_frame.grid(row=0, rowspan=3, column=2, sticky="nswe")

menu_frame.grid_rowconfigure(3, weight=1)

# определение иконок кнопок в активном и неактивном состоянии
file_path = os.path.dirname(os.path.realpath(__file__))

ctk.set_default_color_theme(file_path+"\\source\\violet.json")
home_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\\images\\home_w.png"),
                          dark_image=Image.open(
                              file_path+"\\images\\home_b.png"),
                          size=(24, 24))
home_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\home_b.png"),
                          dark_image=Image.open(
                              file_path+"\images\home_w.png"),
                          size=(24, 24))

cal_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\images\calendar_w.png"),
                         dark_image=Image.open(
                             file_path+"\images\calendar_b.png"),
                         size=(24, 24))
cal_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\calendar_b.png"),
                         dark_image=Image.open(
                             file_path+"\images\calendar_w.png"),
                         size=(24, 24))

loc_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\images\gps_w.png"),
                         dark_image=Image.open(file_path+"\images\gps_b.png"),
                         size=(24, 24))
loc_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\gps_b.png"),
                         dark_image=Image.open(file_path+"\images\gps_w.png"),
                         size=(24, 24))

theme_ing = ctk.CTkImage(light_image=Image.open(file_path+"\images\light.png"),
                         dark_image=Image.open(file_path+"\images\moon.png"),
                         size=(24, 24))

# определение кнопок
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

sa.basic_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

# конфигурация кнопок
home_button.grid(column=0, row=0, sticky="new")
cal_button.grid(column=0, row=1, sticky="new")
loc_button.grid(column=0, row=2, sticky="new")
appear_button.grid(column=0, row=4, sticky="sew")

charts_frame = ctk.CTkFrame(main_frame, fg_color=["white", "black"])

name_textbox_text = ctk.StringVar()
name_textbox_text.set(
    sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")

name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent',
                            font=("Roboto", 36),
                            height=86,
                            textvariable=name_textbox_text,
                            anchor="nw",
                            wraplength=900,
                            justify="left")

main_frame.grid_rowconfigure(2, weight=1)
name_textbox.grid(row=0, column=0, rowspan=1,
                  sticky="new", padx=(54, 0), pady=(33, 0))
charts_frame.grid(row=1, column=0, rowspan=2, sticky="")

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
                               font=("Roboto", 14),
                               anchor="w",
                               justify="left")
loc_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=loc_info_text,
                              wraplength=364,
                              font=("Roboto", 14),
                              anchor="w",
                              justify="left")
cal_info_label = ctk.CTkLabel(charts_frame,
                              width=400,
                              height=250,
                              corner_radius=20,
                              fg_color=["#D9D9D9", "#4A4A4A"],
                              textvariable=cal_info_text,
                              wraplength=364,
                              font=("Roboto", 14),
                              anchor="w",
                              justify="left")

ill_chart_frame = ctk.CTkFrame(
    charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])
cured_chart_frame = ctk.CTkFrame(
    charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])
death_chart_frame = ctk.CTkFrame(
    charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9", "#4A4A4A"])


main_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))
loc_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))
cal_info_label.grid(row=0, column=0, pady=(0, 31), padx=(54, 0))
main_info_label.tkraise()
ill_chart_frame.grid(row=0, column=1, pady=(0, 31), padx=(54, 52))
cured_chart_frame.grid(row=1, column=0, pady=(0, 0), padx=(54, 0))
death_chart_frame.grid(row=1, column=1, pady=(0, 0), padx=(54, 52))

news_frame = ctk.CTkScrollableFrame(
    info_frame, fg_color=["#D9D9D9", "#4A4A4A"])
set_news_frame()

loc_opt_menu = ctk.CTkOptionMenu(info_frame,
                                 width=225,
                                 height=39,
                                 values=sa.regions,
                                 command=option_menu_callback,
                                 font=("Roboto", 15))  # loc_frame
last_ten_box = ctk.CTkCheckBox(info_frame,
                               width=225,
                               text="Последние 10 дней",
                               font=("Roboto", 16),
                               command=last_ten_check_callback)  # loc_frame
# создание меню выбора периода
show_periond_box = ctk.CTkCheckBox(info_frame,
                                   width=225,
                                   text="Указать период",
                                   font=("Roboto", 16),
                                   command=show_period_ckeck_callback)

period_frame = ctk.CTkFrame(master=info_frame, fg_color=[
                            "white", "black"], width=255, height=525,)

calendar_frame = ctk.CTkFrame(master=info_frame, fg_color=[
                              "white", "black"], width=255)  # cal_frame

# создание календаря
month_menu = ctk.CTkOptionMenu(calendar_frame, values=sa.months,
                               font=("Roboto", 14),
                               corner_radius=0,
                               width=120,
                               command=data_optionmenu_callback)
year_menu = ctk.CTkOptionMenu(calendar_frame,
                              values=[],
                              font=("Roboto", 14),
                              corner_radius=0,
                              width=90,
                              command=data_optionmenu_callback)
set_calendar_frame()
set_period_frame()
home_button_callback()
app.mainloop()
