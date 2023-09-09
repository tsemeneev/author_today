import customtkinter
import subprocess
from main import parser


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x400")
app.title("Парсер сайта Author.Today")


def button_function():
    button.destroy()
    label.configure(text="Парсинг начался. Это может занять 3-4 минуты.\n"
                        "Пожалуйста, не закрывайте окно пока парсер не закончит работу")
    app.update()
    parser.main()
    label.configure(text="Парсинг завершен")
    app.update()
    

    
def run_bat_script(script_path):
    process = subprocess.Popen(rf'.\copy_files.bat', shell=True)
    # Вы можете выполнять другие действия во время выполнения скрипта
    process.wait() # Ожидайте завершения процесса


# Use CTkButton instead of tkinter Button
label = customtkinter.CTkLabel(master=app, text="Для того чтобы начать парсинг нажмите кнопку 'Запустить'")
label.pack(pady=150)
button = customtkinter.CTkButton(master=app, text="Запустить", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()