import customtkinter as ctk
from PIL import Image, ImageTk

def home_button_callback():
    home_button.configure(fg_color=color_const)
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color="transparent")
    cal_frame.grid_remove()
    loc_frame.grid_remove()
    info_frame.grid(row=0, column=2, sticky="nse")

def cal_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color=color_const)
    loc_button.configure(fg_color="transparent")
    cal_frame.grid(row=0, column=2, sticky="nse")
    loc_frame.grid_remove()
    info_frame.grid_remove()

def loc_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color=color_const)
    cal_frame.grid_remove()
    loc_frame.grid(row=0, column=2, sticky="nse")
    info_frame.grid_remove()

def appear_button_callback():
    if app._get_appearance_mode()=="light":
        app._set_appearance_mode("dark")
    else:
        app._set_appearance_mode("light") 

app = ctk.CTk()

app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна

app.grid_rowconfigure(0, weight=1)  # определение grid-системы
app.grid_columnconfigure((1), weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, fg_color=("#FFFFFF","#000000"), bg_color=("#FFFFFF","#000000")) #создание основной зоны
info_frame = ctk.CTkScrollableFrame(master=app, width=251, fg_color="#D9D9D9", bg_color="#D9D9D9", border_width=0) #создание зоны новостей
loc_frame = ctk.CTkFrame(master=app, width=251, fg_color="#D9D9D9", bg_color="#D9D9D9")
cal_frame = ctk.CTkFrame(master=app, width=251, fg_color="#D9D9D9", bg_color="#D9D9D9")

menu_frame.grid(row=0, column=0, sticky="nsw") #расположение зоны основной навигации
main_frame.grid(row=0, column=1, sticky="nsew")
info_frame.grid(row=0, column=2, sticky="nse") # инфо-режим стоит по умолчанию при запуске программы

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

color_const = home_button.cget("fg_color") #временное решение для определения цвета в установленной схеме

cal_button = ctk.CTkButton( menu_frame, 
                            width=90, 
                            height=90, 
                            text="Cal",
                            border_width=0,
                            corner_radius=0,
                            border_spacing=0,
                            fg_color='transparent',
                            text_color=("black","red"),
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

app.mainloop()