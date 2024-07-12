import tkinter as tk
from tkinter import ttk, messagebox
from sql_login import SQLLogin
from mssql_screen import MSSQLScreen
from oracle_screen import OracleScreen
import json
import os
import threading
import time

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Login")
        self.root.geometry("500x550")  # 设置初始窗口大小
        self.root.minsize(500, 550)  # 设置最小窗口大小

        self.sql_login = SQLLogin()  # Add this line to create SQLLogin instance
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_login_screen()

    # 添加 on_closing 方法
    def on_closing(self):
        if self.sql_login.connection is not None:
            self.sql_login.connection.close()
            self.sql_login.connection = None
        self.root.destroy()

    def create_login_screen(self):
        self.label_server_type = tk.Label(self.frame, text="Server Type:")
        self.label_server_type.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.server_type_var = tk.StringVar(self.frame)
        self.server_type_var.set("MS SQL Server")  # 默认选择
        self.server_type_menu = tk.OptionMenu(self.frame, self.server_type_var, "MS SQL Server", "Oracle", command=self.update_form)
        self.server_type_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.dynamic_frame = tk.Frame(self.frame)
        self.dynamic_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.grid(row=8, columnspan=3, padx=10, pady=10, sticky="ew")

        self.button_login = tk.Button(self.frame, text="Login", command=self.start_login)
        self.button_login.grid(row=9, columnspan=3, padx=10, pady=10)

        self.load_login_info()
        self.update_form()
        self.frame.columnconfigure(1, weight=1)
        self.dynamic_frame.columnconfigure(1, weight=1)

    def show_login_screen(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.update_form()

    def update_form(self, *args):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        self.entry_widgets = []

        server_type = self.server_type_var.get()

        if server_type == "MS SQL Server":
            self.label_host = tk.Label(self.dynamic_frame, text="Host*:")
            self.label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.entry_host = self.create_entry_widget(self.dynamic_frame, 0, 1)

            self.saved_hosts_var = tk.StringVar(self.dynamic_frame)
            self.saved_hosts_menu = tk.OptionMenu(self.dynamic_frame, self.saved_hosts_var, "")
            self.saved_hosts_menu.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
            self.saved_hosts_var.trace("w", self.host_selected)

            self.label_database = tk.Label(self.dynamic_frame, text="Database/Schema:")
            self.label_database.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.entry_database = self.create_entry_widget(self.dynamic_frame, 1, 1)

            self.label_username = tk.Label(self.dynamic_frame, text="Username:")
            self.label_username.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.entry_username = self.create_entry_widget(self.dynamic_frame, 2, 1)

            self.label_password = tk.Label(self.dynamic_frame, text="Password:")
            self.label_password.grid(row=3, column=0, padx=10, pady=5, sticky="w")
            self.entry_password = self.create_entry_widget(self.dynamic_frame, 3, 1, show="*")

            self.trust_certificate = tk.BooleanVar()
            self.checkbox_trust_certificate = tk.Checkbutton(self.dynamic_frame, text="Trust Server Certificate", variable=self.trust_certificate)
            self.checkbox_trust_certificate.grid(row=4, columnspan=2, padx=10, pady=5, sticky="w")

            self.remember_me = tk.BooleanVar()
            self.checkbox_remember = tk.Checkbutton(self.dynamic_frame, text="Remember Me", variable=self.remember_me)
            self.checkbox_remember.grid(row=5, columnspan=2, padx=10, pady=5, sticky="w")

        elif server_type == "Oracle":
            self.label_host = tk.Label(self.dynamic_frame, text="Host*:")
            self.label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.entry_host = self.create_entry_widget(self.dynamic_frame, 0, 1)

            self.saved_hosts_var = tk.StringVar(self.dynamic_frame)
            self.saved_hosts_menu = tk.OptionMenu(self.dynamic_frame, self.saved_hosts_var, "")
            self.saved_hosts_menu.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
            self.saved_hosts_var.trace("w", self.host_selected)

            self.label_port = tk.Label(self.dynamic_frame, text="Port*:")
            self.label_port.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.entry_port = self.create_entry_widget(self.dynamic_frame, 1, 1)
            self.entry_port.insert(0, "1521")  # Default port for Oracle

            self.label_service_name = tk.Label(self.dynamic_frame, text="Service Name*:")
            self.label_service_name.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.entry_service_name = self.create_entry_widget(self.dynamic_frame, 2, 1)

            self.service_name_or_sid = tk.StringVar(value="Service Name")
            self.radio_service_name = tk.Radiobutton(self.dynamic_frame, text="Service Name", variable=self.service_name_or_sid, value="Service Name")
            self.radio_service_name.grid(row=3, column=0, padx=10, pady=5, sticky="w")
            self.radio_sid = tk.Radiobutton(self.dynamic_frame, text="SID", variable=self.service_name_or_sid, value="SID")
            self.radio_sid.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            self.label_username = tk.Label(self.dynamic_frame, text="Username*:")
            self.label_username.grid(row=4, column=0, padx=10, pady=5, sticky="w")
            self.entry_username = self.create_entry_widget(self.dynamic_frame, 4, 1)

            self.label_password = tk.Label(self.dynamic_frame, text="Password*:")
            self.label_password.grid(row=5, column=0, padx=10, pady=5, sticky="w")
            self.entry_password = self.create_entry_widget(self.dynamic_frame, 5, 1, show="*")

            self.remember_me = tk.BooleanVar()
            self.checkbox_remember = tk.Checkbutton(self.dynamic_frame, text="Remember Me", variable=self.remember_me)
            self.checkbox_remember.grid(row=6, columnspan=2, padx=10, pady=5, sticky="w")

        self.update_host_menu()

    def create_entry_widget(self, parent, row, column, **kwargs):
        entry = tk.Entry(parent, **kwargs)
        entry.grid(row=row, column=column, padx=10, pady=5, sticky="ew")
        entry.bind("<Return>", self.on_enter_pressed)
        self.entry_widgets.append(entry)
        return entry

    def on_enter_pressed(self, event):
        widget = event.widget
        if widget in self.entry_widgets:
            index = self.entry_widgets.index(widget)
            if index < len(self.entry_widgets) - 1:
                self.entry_widgets[index + 1].focus()
            else:
                self.start_login()

    def start_login(self):
        self.button_login.config(state=tk.DISABLED)
        threading.Thread(target=self.login).start()

    def login(self):
        server_type = self.server_type_var.get()
        host = self.entry_host.get()
        remember = self.remember_me.get()

        if server_type == "MS SQL Server":
            database = self.entry_database.get()
            username = self.entry_username.get()
            password = self.entry_password.get()
            trust_certificate = self.trust_certificate.get()

            if host and username and password:
                if remember:
                    self.save_login_info(server_type, host, database, username, password, trust_certificate)
                else:
                    self.clear_login_info(host)

                self.sql_login = SQLLogin()

                self.update_progress(10)
                time.sleep(0.5)  # Simulate progress

                connection_successful = False
                try:
                    self.update_progress(30)
                    time.sleep(0.5)  # Simulate progress
                    self.sql_login.connect_mssql(host, database, username, password, trust_certificate)
                    connection_successful = True
                except Exception as e:
                    messagebox.showerror("Connection Error", f"Failed to connect to {server_type}: {e}")

                self.update_progress(100)
                time.sleep(0.5)  # Simulate progress

                self.sql_login.close_connection()
                self.update_progress(0)

                if connection_successful:
                    self.show_mssql_screen()
            else:
                messagebox.showwarning("Login Info", "Please enter the required fields (Host, Username, Password)")

        elif server_type == "Oracle":
            port = self.entry_port.get()
            service_name = self.entry_service_name.get()
            use_sid = self.service_name_or_sid.get() == "SID"
            username = self.entry_username.get()
            password = self.entry_password.get()

            if host and port and service_name and username and password:
                if remember:
                    self.save_login_info_oracle(server_type, host, port, service_name, username, password)
                else:
                    self.clear_login_info(host)

                self.update_progress(10)
                time.sleep(0.5)  # Simulate progress

                connection_successful = False
                try:
                    self.update_progress(30)
                    time.sleep(0.5)  # Simulate progress
                    self.sql_login.connect_oracle(host, port, service_name, username, password, use_sid)
                    connection_successful = True
                except Exception as e:
                    messagebox.showerror("Connection Error", f"Failed to connect to {server_type}: {e}")

                self.update_progress(100)
                time.sleep(0.5)  # Simulate progress

                if connection_successful:
                    self.show_oracle_screen()
            else:
                messagebox.showwarning("Login Info", "Please enter the required fields (Host, Port, Service Name/SID, Username, Password)")

        self.button_login.config(state=tk.NORMAL)

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def save_login_info(self, server_type, host, database, username, password, trust_certificate):
        if os.path.exists("login_info.json"):
            with open("login_info.json", "r") as f:
                login_info = json.load(f)
        else:
            login_info = {}

        login_info[host] = {
            "server_type": server_type,
            "host": host,
            "database": database,
            "username": username,
            "password": password,
            "trust_certificate": trust_certificate
        }

        with open("login_info.json", "w") as f:
            json.dump(login_info, f)

    def save_login_info_oracle(self, server_type, host, port, service_name, username, password):
        if os.path.exists("login_info.json"):
            with open("login_info.json", "r") as f:
                login_info = json.load(f)
        else:
            login_info = {}

        login_info[host] = {
            "server_type": server_type,
            "host": host,
            "port": port,
            "service_name": service_name,
            "username": username,
            "password": password
        }

        with open("login_info.json", "w") as f:
            json.dump(login_info, f)

    def load_login_info(self):
        if os.path.exists("login_info.json"):
            with open("login_info.json", "r") as f:
                self.login_info = json.load(f)
        else:
            self.login_info = {}

    def clear_login_info(self, host):
        if os.path.exists("login_info.json"):
            with open("login_info.json", "r") as f:
                login_info = json.load(f)
            if host in login_info:
                del login_info[host]
            with open("login_info.json", "w") as f:
                json.dump(login_info, f)
        
        self.update_host_menu()
    
    def update_host_menu(self):
        if hasattr(self, 'saved_hosts_menu'):
            self.saved_hosts_menu['menu'].delete(0, 'end')
            server_type = self.server_type_var.get()
            for host, details in self.login_info.items():
                if details['server_type'] == server_type:
                    self.saved_hosts_menu['menu'].add_command(label=host, command=tk._setit(self.saved_hosts_var, host))
    
    def host_selected(self, *args):
        host = self.saved_hosts_var.get()
        if host in self.login_info:
            user_info = self.login_info[host]
            server_type = user_info["server_type"]
            self.server_type_var.set(server_type)
            self.update_form()
            self.entry_host.delete(0, tk.END)  # Move this line here
            self.entry_host.insert(0, user_info["host"])
            if server_type == "MS SQL Server":
                self.entry_database.delete(0, tk.END)
                self.entry_database.insert(0, user_info["database"])
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, user_info["username"])
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, user_info["password"])
                self.trust_certificate.set(user_info["trust_certificate"])
            elif server_type == "Oracle":
                self.entry_port.delete(0, tk.END)
                self.entry_port.insert(0, user_info["port"])
                service_name_or_sid = user_info["service_name"]
                if "SID" in service_name_or_sid:
                    self.service_name_or_sid.set("SID")
                    self.entry_service_name.delete(0, tk.END)
                    self.entry_service_name.insert(0, service_name_or_sid.split("=")[1].strip(')'))
                else:
                    self.service_name_or_sid.set("Service Name")
                    self.entry_service_name.delete(0, tk.END)
                    self.entry_service_name.insert(0, service_name_or_sid)
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, user_info["username"])
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, user_info["password"])

    def show_mssql_screen(self):
        self.frame.pack_forget()
        MSSQLScreen(self.root, self)

    def show_oracle_screen(self):
        self.frame.pack_forget()
        OracleScreen(self.root, self)

# Create the main window
root = tk.Tk()
app = LoginApp(root)
root.mainloop()
