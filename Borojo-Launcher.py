from tkinter import Tk, Label, Button, Entry, PhotoImage, Toplevel, ttk
import minecraft_launcher_lib
import subprocess
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainApp():
    def __init__(self, login):
        self.login = login
        self.login.title("Borojo Launcher - Login")
        self.login.geometry("300x400")
        self.login.resizable(0,0)
        self.login.iconbitmap(resource_path("gatopanico.ico"))
        
        self.create_widgets()
        
    def name_account(self):
        if self.username_entry.get().strip() == "":
            Label(self.login, text="Porfavor ingrese un nombre", font=("Cascadia Mono", 12), bg="#909090", fg="#ff0000", width=26).place(x=30, y=330)
        else:
            self.open_main()
    
    def versions(self):
        list_versions = minecraft_launcher_lib.utils.get_available_versions(self.minecraft_directory)
        all_versions = []
        for version in list_versions:
            if version["type"] == "release":
                all_versions.append(version["id"])
                
            self.version_select.config(values=all_versions)
            
    def versions_installed(self):
        list_versions_installed = minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_directory)
        all_versions_installed = []
        for versions in list_versions_installed:
            all_versions_installed.append(versions["id"])
            
        self.version_installed_selected.config(values=all_versions_installed)
            
    def set_status(self, status: str):
        print(status)
            
    def set_progress(self, progress: int):
        if self.current_max != 0:
            self.progress_bar["value"] = progress
            self.main.update()

    def set_max(self, new_max: int):
        global current_max
        self.current_max = new_max
        self.progress_bar["maximum"] = new_max

    def open_main(self):
        self.main = Toplevel(self.login)
        self.main.title("Borojo Launcher - Main")
        self.main.geometry("400x600")
        self.main.resizable(0,0)
        self.main.iconbitmap(resource_path("gatopanico.ico"))
        self.login.withdraw()
        
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        self.user_name = self.username_entry.get().strip()
        self.current_max = 0
        self.callback = {
                        "setStatus": self.set_status,
                        "setProgress": self.set_progress,
                        "setMax": self.set_max
                        }
        self.options = {
                        "username":self.user_name,
                        "uuid": "",
                        "token": "",
                        "jvmArguments": ["-Xmx2G", "-Xms2G"],
                        "launcherName": "Borojo Launcher",
                        "launcherVersion": "1.0",
                        }
        
        self.create_widgets2()
        
    def install_minecraft(self):
        selected_version = self.version_select.get()
        if selected_version:
            minecraft_launcher_lib.install.install_minecraft_version(self.version_select.get(), self.minecraft_directory, callback=self.callback)
        else:
            Label(self.main, text="Porfavor ingrese una version", padx=22, font=("Cascadia Mono", 10), bg="#909090", fg="#ff0000", width=25).place(x=75, y=410)

    def installed_minecraft(self):
        selected_installed_version = self.version_installed_selected.get()
        if selected_installed_version:
            self.run_minecraft(selected_installed_version)
        else:
            Label(self.main, text="Porfavor ingrese una version", padx=22, font=("Cascadia Mono", 10), bg="#909090", fg="#ff0000", width=25).place(x=75, y=410)

    def run_minecraft(self, version):
        self.minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, self.minecraft_directory, self.options)
        subprocess.run(self.minecraft_command)
        
        self.progress_bar["value"] = 0
        self.main.update()
        
    def start(self):
        self.install_minecraft()
        self.progress_bar["value"]+=self.current_max
        
    def start2(self):
        self.installed_minecraft()
        self.progress_bar["value"]+=self.current_max
        
    def create_widgets(self):
        self.background = PhotoImage(file=resource_path("background.png"))
        self.background_label = Label(self.login, image=self.background)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.gatopan = PhotoImage(file=resource_path("gatopan.png"))
        self.gatopan_label = Label(self.login, image=self.gatopan, bd=0)
        self.gatopan_label.place(x=50, y=50)
        
        self.username_label = Label(self.login, text="Username:", font=("Cascadia Mono", 12),)
        self.username_entry = Entry(self.login, font=("Cascadia Mono", 12), width=12)
        self.username_button = Button(self.login, text="Login", font=("Cascadia Mono", 12), command=self.name_account)
        self.username_label.place(x=50, y=260)
        self.username_entry.place(x=140, y=260)
        self.username_button.place(x=120, y=290)
        
    def create_widgets2(self):
        self.background2 = PhotoImage(file=resource_path("background2.png"))
        self.background2_label = Label(self.main, image=self.background2)
        self.background2_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.gatortuga = PhotoImage(file=resource_path("gatortuga.png"))
        self.gatortuga_label = Label(self.main, image=self.gatortuga, bd=0)
        self.gatortuga_label.place(x=75, y=50)
        
        self.username_selected = Label(self.main, text="Usuario: " + self.username_entry.get(), font=("Cascadia Mono", 12))
        self.versiones_label = Label(self.main, text="Instalar: ", font=("Cascadia Mono", 12), height=1)
        self.version_select = ttk.Combobox(self.main, values = self.versions, font=("Cascadia Mono", 12), width=14)
        self.version_installed = Label(self.main, text="Instaladas: ", font=("Cascadia Mono", 12), height=1)
        self.version_installed_selected = ttk.Combobox(self.main, values = self.versions_installed, font=("Cascadia Mono", 12), width=12)
        self.download_button = Button(self.main, text="Descargar", font=("Cascadia Mono", 16), command=self.start)
        self.play_button = Button(self.main, text="Jugar", font=("Cascadia Mono", 16), command=self.start2)
        self.progress_bar = ttk.Progressbar(self.main, orient="horizontal", length=250)
        
        self.username_selected.place(x=75, y=310)
        self.versiones_label.place(x=75, y=340)
        self.version_select.place(x=175, y=340)
        self.version_installed.place(x=75, y=370)
        self.version_installed_selected.place(x=193, y=370)
        self.download_button.place(x=75, y=470)
        self.play_button.place(x=247, y=470)
        self.progress_bar.place(x=75, y=550)
        
        self.versions_installed()
        self.versions()
        
        
        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.login.destroy()


if __name__ == "__main__":
    login = Tk()
    app = MainApp(login)
    login.mainloop()