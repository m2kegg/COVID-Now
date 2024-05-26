import customtkinter as ctk
from PIL import Image
from datetime import datetime 
import samples as sa
import os
from calendar import monthrange

def home_button_callback():
    home_button.configure(fg_color=sa.basic_color, image=home_img_a)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color="transparent", image=loc_img_d)

    info_frame.grid_rowconfigure((0,1,2),weight=0)
    info_frame.grid_columnconfigure(0, weight=0)

    info_frame.grid_rowconfigure(0,weight=1)
    info_frame.grid_columnconfigure(0, weight=1)

    news_textbox.grid(row=0, column=0, padx=(10,10), pady=(15,15) ,sticky="nsew")
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

    news_textbox.grid_remove()
    loc_opt_menu.grid_remove()
    last_ten_box.grid_remove()
    calendar_frame.grid_configure(row=0, column=0, padx=(10,10),pady=(50,0), sticky="n")

    name_textbox_text.set(sa.cal_main_text+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})
    main_info_label.configure(text=sa.frame_cal_text)

def loc_button_callback():
    home_button.configure(fg_color="transparent", image=home_img_d)
    cal_button.configure(fg_color="transparent", image=cal_img_d)
    loc_button.configure(fg_color=sa.basic_color, image=loc_img_a)

    info_frame.grid_rowconfigure((0,1,2),weight=0)
    info_frame.grid_columnconfigure(0, weight=1)

    news_textbox.grid_remove()
    loc_opt_menu.grid_configure(row=0, column=0, padx=(13,13),pady=(33,0), sticky="ew")
    last_ten_box.grid_configure(row=1, column=0, padx=(13,13), pady=(40,0), sticky="")
    calendar_frame.grid_configure(row=2, column=0, padx=(10,10),pady=(50,0))

    name_textbox_text.set(sa.loc_main_text+loc_opt_menu.get()+" на "+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})
    main_info_label.configure(text=sa.frame_loc_text)


def appear_button_callback():
    if ctk.get_appearance_mode().lower()=="light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light") 

def option_menu_callback(choice):
    name_textbox_text.set(sa.loc_main_text+choice+" на "+'%(day)02d.%(month)02d.%(year)d' %{'day':sa.day, 'month':sa.month,'year':sa.year})

def data_optionmenu_callback(choice):   
    year_i = int(year_menu.get())
    month_i = sa.months.index(month_menu.get())+1
    first_info = monthrange(year_i, month_i)
    for i in range(0,first_info[0]):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state="disabled", text='')
    for i in range(first_info[0], first_info[1]+first_info[0]):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state="normal", text=str(i-first_info[0]+1),
                        command=lambda m=i-first_info[0]+1:date_button_callback(m))
    for i in range(first_info[1]+first_info[0], 42):
        button = calendar_frame.grid_slaves(row=2+i//7, column=i%7)[0]
        button.configure(state="disabled", text='')
    if (choice != -1):
        date_button_callback(1)
    else:
        calendar_frame.grid_slaves(row=2+(sa.day+first_info[0]-1)//7, column=(sa.day+first_info[0]-1)%7)[0].configure(border_width=1)


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



def set_news_frame():
    menu_new_val = [""] # переменная которая будет хранить полученные новости
    for tmp_text in menu_new_val:
        news_textbox.insert(ctk.END,"\n\n"+tmp_text)
    news_textbox.configure(state="disabled")
    
def set_calendar_frame():
    year_val = []
    datetime_str = datetime.today().strftime
    for year in range(2019, int(datetime_str("%Y"))+1):
        year_val.append(str(year))
    for i,name in enumerate(sa.week_name):
        week_label = ctk.CTkLabel(calendar_frame, text=name,font=("Roboto", 12), text_color="white")
        week_label.grid(row=1, column=i)

    month_menu.grid(row=0, column=0, columnspan=4)
    year_menu.grid(row=0, column=4, columnspan=3)
    for i in range (0, 42):
        button = ctk.CTkButton(calendar_frame, text="", 
                               width=20, 
                               state="disabled", 
                               fg_color="transparent",
                               bg_color="transparent",
                               border_color="black",
                               
                               )
        button.grid(row=2+i//7, column=i%7)
    sa.day=int(datetime_str("%d"))
    sa.month=int(datetime_str("%m"))
    sa.year=int(datetime_str("%Y"))
    year_menu.configure(values=year_val)
    year_menu.set(year_val[-1])
    month_menu.set(sa.months[int(sa.month)-1])
    data_optionmenu_callback(-1)



app = ctk.CTk()
app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна

app.grid_rowconfigure((0,1), weight=1)  # определение grid-системы
app.grid_columnconfigure(2, weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color="#FFFFFF", bg_color="#FFFFFF") #создание основной зоны
info_frame = ctk.CTkFrame(master=app, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны новостей

menu_frame.grid(row=0, rowspan=3, column=0, sticky="ns") #расположение зоны основной навигации
main_frame.grid(row=0,rowspan=3, column=1, sticky="nsew")
info_frame.grid(row=0,rowspan=3, column=2, sticky="nswe") # инфо-режим стоит по умолчанию при запуске программы

menu_frame.grid_rowconfigure(3,weight=1)

# определение иконок кнопок в активном и неактивном состоянии
file_path = os.path.dirname(os.path.realpath(__file__))

home_img_a = ctk.CTkImage(light_image=Image.open(file_path+"\images\home_w.png"),
                       dark_image=Image.open(file_path+"\images\home_b.png"),
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

# конфигурация кнопок
home_button.grid(column=0,row=0, sticky="new")
cal_button.grid(column=0,row=1, sticky="new")
loc_button.grid(column=0,row=2, sticky="new")
appear_button.grid(column=0,row=4, sticky="sew")

charts_frame=ctk.CTkFrame(main_frame,fg_color="#FFFFFF")

name_textbox_text = ctk.StringVar()
name_textbox_text.set(sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")

name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent', 
                            font=("Roboto",36),
                            height=43,
                            textvariable=name_textbox_text,
                            anchor="nw",
                            wraplength=900,
                            justify="left")

name_textbox.grid(row= 0,column=0, sticky="ew",padx=(54,0), pady=(33,0))
charts_frame.grid(row=1,column=0)

main_info_label = ctk.CTkLabel(charts_frame, width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
ill_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
cured_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
death_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")

main_info_label.grid(row= 0,column=0,pady=(56,0), padx=(54,0))
ill_chart_frame.grid(row= 0,column=1, pady=(56,0), padx=(54,52))
cured_chart_frame.grid(row= 1,column=0, pady=(31,0), padx=(54,0))
death_chart_frame.grid(row= 1,column=1, pady=(31,0), padx=(54,52))

main_info_label.configure(
    text=sa.frame_home_text,
    wraplength=364,
    font=("Roboto",14),
    anchor="w",
    justify="left")

news_textbox = ctk.CTkTextbox(info_frame,font=("Roboto Mono",14), fg_color="#FFFFFF", corner_radius=20)
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
                              font=("Roboto",16))#loc_frame

calendar_frame = ctk.CTkFrame(master=info_frame, fg_color=sa.basic_color, width=255) #cal_frame

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