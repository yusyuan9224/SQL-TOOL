import tkinter as tk

class MSSQLScreen:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.label = tk.Label(self.frame, text="Welcome to MS SQL Server", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button_back = tk.Button(self.frame, text="Back to Login", command=self.back_to_login)
        self.button_back.pack(pady=20)

    def back_to_login(self):
        # Close the SQL connection
        if self.sql_login.connection is not None:
            self.sql_login.connection.close()
            self.sql_login.connection = None
        
        self.frame.pack_forget()
        self.login_app.show_login_screen()

    # 添加 on_closing 方法
    def on_closing(self):
        if self.login_app.sql_login.connection is not None:
            self.login_app.sql_login.connection.close()
            self.login_app.sql_login.connection = None
        self.root.destroy()
