import customtkinter as ctk
import ctkchart as chart
from PIL import Image
from datetime import datetime 
import samples as sa

def home_button_callback():
    home_button.configure(fg_color=sa.basic_color)
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color="transparent")
    cal_frame.grid_remove()
    loc_frame.grid_remove()
    info_frame.grid(row=0, column=2, sticky="nsew")

    name_textbox.configure(text=sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}")
    main_info_label.configure(text=sa.frame_home_text)

def cal_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color=sa.basic_color)
    loc_button.configure(fg_color="transparent")
    cal_frame.grid(row=0, column=2, sticky="nsew")
    loc_frame.grid_remove()
    info_frame.grid_remove()

    name_textbox.configure(text=sa.cal_main_text)
    main_info_label.configure(text=sa.frame_cal_text)

def loc_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color=sa.basic_color)
    cal_frame.grid_remove()
    loc_frame.grid(row=0, column=2, sticky="nsew")
    info_frame.grid_remove()

    name_textbox.configure(text=sa.loc_main_text+loc_opt_box.get())
    main_info_label.configure(text=sa.frame_loc_text)


def appear_button_callback():
    if ctk.get_appearance_mode().lower()=="light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light") 

def option_box_callback(choice):
    name_textbox.configure(text=sa.loc_main_text+choice)

app = ctk.CTk()
app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна

app.grid_rowconfigure(0, weight=1)  # определение grid-системы
app.grid_columnconfigure(2, weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color="#FFFFFF", bg_color="#FFFFFF") #создание основной зоны
info_frame = ctk.CTkScrollableFrame(master=app, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны новостей
loc_frame = ctk.CTkFrame(master=app, fg_color="#D9D9D9", bg_color="#D9D9D9")
cal_frame = ctk.CTkFrame(master=app, fg_color="#D9D9D9", bg_color="#D9D9D9")

menu_frame.grid(row=0, column=0, sticky="ns") #расположение зоны основной навигации
main_frame.grid(row=0, column=1, sticky="nsew")
info_frame.grid(row=0, column=2, sticky="nswe") # инфо-режим стоит по умолчанию при запуске программы

menu_frame.grid_rowconfigure(3,weight=1)

home_button = ctk.CTkButton( menu_frame, 
                            width=90, 
                            height=90,
                            text='Home',
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            text_color=("black","white"),
                            command=home_button_callback
                           )

cal_button = ctk.CTkButton( menu_frame, 
                            width=90, 
                            height=90, 
                            text="Cal",
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            fg_color='transparent',
                            text_color=("black","white"),
                            command=cal_button_callback)

loc_button = ctk.CTkButton(menu_frame, 
                            width=90, 
                            height=90, 
                            text="Loc",
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            fg_color='transparent',
                            text_color=("black","white"),
                            command=loc_button_callback)

appear_button = ctk.CTkButton(menu_frame, 
                            width=90, 
                            height=90, 
                            text="*",
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            fg_color='transparent',
                            text_color=("black","white"),
                            command=appear_button_callback)

home_button.grid(column=0,row=0, sticky="new")
cal_button.grid(column=0,row=1, sticky="new")
loc_button.grid(column=0,row=2, sticky="new")
appear_button.grid(column=0,row=4, sticky="sew")

charts_frame=ctk.CTkFrame(main_frame,fg_color="#FFFFFF")
name_textbox = ctk.CTkLabel(main_frame,
                            fg_color='transparent', 
                            font=("Roboto",36),
                            height=43,
                            text=sa.home_main_text+f"{datetime.today().strftime('%d.%m.%Y')}",
                            anchor="nw")
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

loc_opt_box= ctk.CTkComboBox(loc_frame,
                                 width=225,
                                 height=39, 
                                 values=sa.regions, 
                                 command=option_box_callback)

last_ten_box = ctk.CTkCheckBox(loc_frame,
                              width=225,
                              text="Последние 10 дней")

loc_frame.grid_columnconfigure(0,weight=1)

loc_opt_box.grid(row=0, column=0, padx=(13,13),pady=(33,0), sticky="ew")
last_ten_box.grid(row=1, column=0, pady=(40,0), sticky="ew")
app.mainloop()