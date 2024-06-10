import customtkinter as ctk
from PIL import Image
from datetime import datetime 
import samples as sa
import os
from calendar import monthrange


# Про конфигурацию текста в прямоугольниках - теперь для каждого экрана есть свой собственный Label-объект
# с настроенной переменной. main_info_label -> main_info_text. При помощи метода .set для text переменных
# можно динамически менять содержание текста label без метода configure.


def home_button_callback():
    home_button.configure(fg_color=sa.basic_color, image=home_img_a)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0,1,2),weight=0)
    info_frame.grid_columnconfigure(0, weight=0)

    info_frame.grid_rowconfigure(0,weight=1)
    info_frame.grid_columnconfigure(0, weight=1)

    main_info_label.tkraise()

    news_frame.grid(row=0, column=0 ,sticky="nsew") 
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    calendar_frame.grid_remove()

    name_textbox_text.set(sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")
    main_info_label.configure(text=sa.frame_home_text)

def cal_button_callback():
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color=sa.basic_color, image=cal_img_a)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0,1,2),weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    cal_info_label.tkraise()

    news_frame.grid_remove()
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    calendar_frame.grid_configure(row=0, column=0, padx=(10,10),pady=(50,0), sticky="new")

    name_textbox_text.set(sa.cal_main_text+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})
    main_info_label.configure(text=sa.frame_cal_text)

def loc_button_callback():
    sa.frame_loc_text = "WORKED"
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color=sa.basic_color, image=loc_img_a)

    info_frame.grid_rowconfigure((0,1,2),weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    loc_info_label.tkraise()

    news_frame.grid_remove()
    loc_opt_menu.grid_configure(row=0, column=0, padx=(13,13),pady=(33,0), sticky="ew")
    last_ten_box.grid_configure(row=1, column=0, padx=(13,13), pady=(40,0), sticky="")
    calendar_frame.grid_configure(row=2, column=0, padx=(10,10),pady=(50,0))

    last_ten_box.deselect()
    name_textbox_text.set(sa.loc_main_text+loc_opt_menu.get()+" на "+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})
    main_info_label.configure(text=sa.frame_loc_text)


def appear_button_callback():
    if ctk.get_appearance_mode().lower()=="light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")
    sa.basic_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"] 

def option_menu_callback(choice):
    name_textbox_text.set(sa.loc_main_text+choice+" на "+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})

def data_optionmenu_callback(choice):
  
    year_i = int(year_menu.get())
    month_i = sa.months.index(month_menu.get())+1
    first_info = monthrange(year_i, month_i)
    day_f, day_s = 0,0
    for i in range(0,first_info[0]):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state="disabled", text='')
    for i in range(first_info[0], first_info[1]+first_info[0]):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state=is_day_exist(i-first_info[0]+1, month_i, year_i), text=str(i-first_info[0]+1),
                        command=lambda m=i-first_info[0]+1:date_button_callback(m ))
        
    for i in range(first_info[1]+first_info[0], 42):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state="disabled", text='')
    # if (choice != -1):
    #    date_button_callback(1)
    #else:
    #    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(sa.day+first_info[0]-1)%7)[0].configure(border_width=1)


def date_button_callback(choice):
    first_info = monthrange(sa.year, sa.month)
    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(sa.day+first_info[0]-1)%7)[0].configure(border_width=0)
    # получает нажатую на календаре кнопку даты и разбирает её, записывает в файл констант
    sa.day = choice
    sa.month = sa.months.index(month_menu.get())+1
    sa.year = int(year_menu.get())
    first_info = monthrange(sa.year, sa.month)
    text_tmp=str(name_textbox_text.get())[:-10]
    calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(sa.day+first_info[0]-1)%7)[0].configure(border_width=1)
    name_textbox_text.set(text_tmp+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})

def last_ten_check_callback():
    if last_ten_box.get():
        calendar_frame.grid_remove()
        text_tmp=str(name_textbox_text.get())[:-10]
        name_textbox_text.set(text_tmp+"последние 10 дней")
    else:
        calendar_frame.grid_configure(row=2, column=0, padx=(10,10),pady=(50,0))
        text_tmp=str(name_textbox_text.get())[:-17]
        name_textbox_text.set(text_tmp+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})

def set_news_frame():
    menu_new_val = ["https://www.yandex.ru/search/?text=ctk+textbox+for+links&lr=213", "Вакцина «Спутник» от коронавируса для подростков может поступить в оборот через два месяца"] # переменная которая будет хранить полученные новости
    news_frame.grid_columnconfigure(0, weight=1)
    for i, tmp_text in enumerate(menu_new_val):
        label = ctk.CTkTextbox(news_frame,
                            height=120,
                            
                            font=("Roboto Mono",13), 
                            fg_color=["white","black"], 
                            corner_radius=20,
                             )
        label.insert(ctk.END, tmp_text)
        label.configure(state="disabled")
        label.grid(row=i, column=0, padx=(10,15), pady=(40,0), sticky='ew')

    
    
def set_calendar_frame():
    calendar_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
    year_val = []
    datetime_str = datetime.today().strftime
    for year in range(2020, int(datetime_str("%Y"))+1):
        year_val.append(str(year))
    for i,name in enumerate(sa.week_name):
        week_label = ctk.CTkLabel(calendar_frame, text=name,font=("Roboto", 12), text_color=["black","white"])
        week_label.grid(row=1, column=i,sticky='ew' )

    month_menu.grid(row=0, column=0, columnspan=4, sticky='ew')
    year_menu.grid(row=0, column=4, columnspan=3, sticky='ew')
    for i in range (0, 42):
        button = ctk.CTkButton(calendar_frame, text="", 
                               width=20, 
                               state="disabled", 
                               fg_color="transparent",
                               bg_color="transparent",
                               border_color=["black","white"],
                               text_color=["black","white"]
                               )
        button.grid(row=2+i//7, column=i%7,sticky='ew' )
    sa.day=int(datetime_str("%d"))
    sa.month=int(datetime_str("%m"))
    sa.year=int(datetime_str("%Y"))
    year_menu.configure(values=year_val)
    year_menu.set(year_val[-1])
    month_menu.set(sa.months[int(sa.month)-1])
    data_optionmenu_callback(-1)

def is_day_exist(day: int, month: int, year: int):


    now_date = datetime(year, month, day)
    if now_date < datetime(2020, 3,27) or now_date>datetime.today():
        return "disabled"
    if now_date <= datetime(2023, 5, 15):
        return "normal"
    if now_date > datetime(2023, 5, 16) and now_date.weekday()==1:
        return "normal"

    return "disabled" #функция определяющая имеет ли день статистику или нет, требует доработки


app = ctk.CTk()
app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна

app.grid_rowconfigure((0,1), weight=1)  # определение grid-системы
app.grid_columnconfigure(2, weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color=["#D9D9D9","#4A4A4A"], bg_color=["#D9D9D9","#4A4A4A"]) #создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color=["white","black" ], bg_color=["white","black" ]) #создание основной зоны
info_frame = ctk.CTkFrame(master=app, fg_color=["#D9D9D9","#4A4A4A"], bg_color=["#D9D9D9","#4A4A4A"]) #создание зоны новостей

menu_frame.grid(row=0, rowspan=3, column=0, sticky="ns") #расположение зоны основной навигации
main_frame.grid(row=0,rowspan=3, column=1, sticky="nsew")
info_frame.grid(row=0,rowspan=3, column=2, sticky="nswe") # инфо-режим стоит по умолчанию при запуске программы

menu_frame.grid_rowconfigure(3,weight=1)

# определение иконок кнопок в активном и неактивном состоянии
file_path = os.path.dirname(os.path.realpath(__file__))

ctk.set_default_color_theme(file_path+"\\source\\violet.json")
home_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\\images\\home_w.png"),
                       dark_image=Image.open(file_path+"\\images\\home_b.png"),
                        size=(24,24))
home_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\home_b.png"),
                       dark_image=Image.open(file_path+"\images\home_w.png"),
                        size=(24,24))

cal_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\images\calendar_w.png"),
                       dark_image=Image.open(file_path+"\images\calendar_b.png"),
                        size=(24,24))
cal_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\calendar_b.png"),
                       dark_image=Image.open(file_path+"\images\calendar_w.png"),
                        size=(24,24))

loc_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\images\gps_w.png"),
                       dark_image=Image.open(file_path+"\images\gps_b.png"),
                        size=(24,24))
loc_img_d = ctk.CTkImage(light_image=Image.open(file_path+"\images\gps_b.png"),
                       dark_image=Image.open(file_path+"\images\gps_w.png"),
                        size=(24,24))

theme_ing = ctk.CTkImage(light_image=Image.open(file_path+"\images\light.png"),
                       dark_image=Image.open(file_path+"\images\moon.png"),
                        size=(24,24))

# определение кнопок
home_button = ctk.CTkButton( menu_frame, 
                            width=90, 
                            height=90,
                            text='',
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            text_color=("black","white"),
                            command=home_button_callback,
                            image=home_img_a
                           )

cal_button = ctk.CTkButton( menu_frame, 
                            width=90, 
                            height=90, 
                            text="",
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            fg_color='transparent',
                            text_color=("black","white"),
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
                            text_color=("black","white"),
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
                            text_color=("black","white"),
                            command=appear_button_callback,
                            image=theme_ing)

sa.basic_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]

# конфигурация кнопок
home_button.grid(column=0,row=0, sticky="new")
cal_button.grid(column=0,row=1, sticky="new")
loc_button.grid(column=0,row=2, sticky="new")
appear_button.grid(column=0,row=4, sticky="sew")

charts_frame=ctk.CTkFrame(main_frame,fg_color=["white","black" ])

name_textbox_text = ctk.StringVar()
name_textbox_text.set(sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")

name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent', 
                            font=("Roboto",36),
                            height=86 ,
                            textvariable=name_textbox_text,
                            anchor="nw",
                            wraplength=900,
                            justify="left")

main_frame.grid_rowconfigure(2, weight=1)
name_textbox.grid(row= 0,column=0, rowspan=1,sticky="new",padx=(54,0), pady=(33,0))
charts_frame.grid(row=1,column=0, rowspan=2, sticky="")

main_info_text= ctk.StringVar()
loc_info_text= ctk.StringVar()
cal_info_text= ctk.StringVar()
main_info_text.set(sa.frame_home_text)
loc_info_text.set(sa.frame_loc_text)
cal_info_text.set(sa.frame_cal_text)

main_info_label = ctk.CTkLabel(charts_frame, 
                               width=400, 
                               height=250, 
                               corner_radius=20, 
                               fg_color=["#D9D9D9","#4A4A4A"], 
                               textvariable=main_info_text,
                               wraplength=364,
                               font=("Roboto",14),
                               anchor="w",
                               justify="left")
loc_info_label = ctk.CTkLabel(charts_frame, 
                              width=400, 
                              height=250, 
                              corner_radius=20, 
                              fg_color=["#D9D9D9","#4A4A4A"], 
                              textvariable=loc_info_text,
                              wraplength=364,
                               font=("Roboto",14),
                               anchor="w",
                               justify="left")
cal_info_label = ctk.CTkLabel(charts_frame, 
                              width=400, 
                              height=250, 
                              corner_radius=20, 
                              fg_color=["#D9D9D9","#4A4A4A"], 
                              textvariable=cal_info_text,
                              wraplength=364,
                               font=("Roboto",14),
                               anchor="w",
                               justify="left")

ill_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9","#4A4A4A"])
cured_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9","#4A4A4A"])
death_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color=["#D9D9D9","#4A4A4A"])



main_info_label.grid(row= 0,column=0,pady=(0,31), padx=(54,0))
loc_info_label.grid(row= 0,column=0,pady=(0,31), padx=(54,0))
cal_info_label.grid(row= 0,column=0,pady=(0,31), padx=(54,0))
main_info_label.tkraise()
ill_chart_frame.grid(row= 0,column=1, pady=(0,31), padx=(54,52))
cured_chart_frame.grid(row= 1,column=0, pady=(0,0), padx=(54,0))
death_chart_frame.grid(row= 1,column=1, pady=(0,0), padx=(54,52))

news_frame = ctk.CTkScrollableFrame(info_frame,fg_color=["#D9D9D9","#4A4A4A"] )
set_news_frame()

loc_opt_menu= ctk.CTkOptionMenu(info_frame,
                                 width=225,
                                 height=39, 
                                 values=sa.regions, 
                                 command=option_menu_callback,
                                 font=("Roboto",15)) #loc_frame
last_ten_box = ctk.CTkCheckBox(info_frame,
                              width=225,
                              text="Последние 10 дней",
                              font=("Roboto",16),
                              command=last_ten_check_callback)#loc_frame

calendar_frame = ctk.CTkFrame(master=info_frame, fg_color=["white", "black"], width=255) #cal_frame

#создание календаря
month_menu = ctk.CTkOptionMenu(calendar_frame,values=sa.months, 
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
home_button_callback()
app.mainloop()