import customtkinter as ctk
import ctkchart as chart
from PIL import Image

def home_button_callback():
    home_button.configure(fg_color=color_const)
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color="transparent")
    cal_frame.grid_remove()
    loc_frame.grid_remove()
    info_frame.grid(row=0, column=2, sticky="nsew")

def cal_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color=color_const)
    loc_button.configure(fg_color="transparent")
    cal_frame.grid(row=0, column=2, sticky="nsew")
    loc_frame.grid_remove()
    info_frame.grid_remove()

def loc_button_callback():
    home_button.configure(fg_color="transparent")
    cal_button.configure(fg_color="transparent")
    loc_button.configure(fg_color=color_const)
    cal_frame.grid_remove()
    loc_frame.grid(row=0, column=2, sticky="nsew")
    info_frame.grid_remove()

def appear_button_callback():
    if ctk.get_appearance_mode().lower()=="light":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light") 

app = ctk.CTk()
app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна


app.grid_rowconfigure(0, weight=1)  # определение grid-системы
app.grid_columnconfigure((2), weight=1)

menu_frame = ctk.CTkFrame(master=app, width=90, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны основной навигации
main_frame = ctk.CTkFrame(master=app, width=939, fg_color="#FFFFFF", bg_color="#FFFFFF") #создание основной зоны
info_frame = ctk.CTkScrollableFrame(master=app, fg_color="#D9D9D9", bg_color="#D9D9D9", border_width=0) #создание зоны новостей
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

color_const = home_button.cget("fg_color") #временное решение для определения цвета в установленной схеме

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

main_info_label = ctk.CTkLabel(charts_frame, width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
ill_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
cured_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")
death_chart_frame = ctk.CTkFrame(charts_frame,  width=400, height=250, corner_radius=20, fg_color="#D9D9D9")

name_textbox = ctk.CTkTextbox(main_frame,fg_color='transparent', font=("Roboto",36), height=43)
name_textbox.insert("0.0","Данные o COVID-19 на сегодня, <дата>")


name_textbox.grid(row= 0,column=0, sticky="ew",padx=(54,0), pady=(33,0))
charts_frame.grid(row=1,column=0,sticky="")

main_info_label.grid(row= 0,column=0, sticky="",pady=(56,0), padx=(54,0))
ill_chart_frame.grid(row= 0,column=1, sticky="",pady=(56,0), padx=(54,52))
cured_chart_frame.grid(row= 1,column=0, sticky="",pady=(31,0), padx=(54,0))
death_chart_frame.grid(row= 1,column=1, sticky="",pady=(31,0), padx=(54,52))

app.mainloop()