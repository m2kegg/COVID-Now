import customtkinter as tk

app = tk.CTk()

app.title("COVID Now")   
app.geometry("1280x720") # временное решение создания размера окна

app.grid_rowconfigure(0, weight=1)  # определение grid-системы
app.grid_columnconfigure(0, weight=1)

menu_frame = tk.CTkFrame(master=app, width=90, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны основной навигации
menu_frame.grid(row=0, column=0, sticky="nsw") #расположение зоны основной навигации

main_frame = tk.CTkFrame(master=app, fg_color="#FFFFFF", bg_color="#FFFFFF") #создание основной зоны
main_frame.grid(row=0, column=1, sticky="nswe")

info_frame = tk.CTkFrame(master=app, width=251, fg_color="#D9D9D9", bg_color="#D9D9D9") #создание зоны новостей
info_frame.grid(row=0, column=1, sticky="nse")
