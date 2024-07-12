import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle
from oracle_functions.function1 import Function1Window

class OracleScreen:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app
        self.sql_login = login_app.sql_login  # Ensure sql_login is accessible
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.label = tk.Label(self.frame, text="Welcome to Oracle Database", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Create a new frame for the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.button_query = tk.Button(self.button_frame, text="Execute SQL Query", command=self.open_query_window)
        self.button_query.pack(side=tk.LEFT, padx=10)

        self.button_function1 = tk.Button(self.button_frame, text="Function 1", command=self.open_function1_window)
        self.button_function1.pack(side=tk.LEFT, padx=10)

        # Create a frame for the Treeview and Scrollbars
        self.tree_frame = tk.Frame(self.frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)

        # Add a horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)

        self.button_back = tk.Button(self.frame, text="Back to Login", command=self.back_to_login)
        self.button_back.pack(pady=20)

        self.tree.bind("<Configure>", self.on_tree_configure)

        # Variables for pagination
        self.page_size = 100  # Number of rows to load per page
        self.current_page = 0
        self.rows = []
        self.columns = []

    def open_query_window(self):
        self.query_window = tk.Toplevel(self.root)
        self.query_window.title("Execute SQL Query")

        self.label_query = tk.Label(self.query_window, text="Enter SQL Query:")
        self.label_query.pack(pady=5)

        self.text_query = tk.Text(self.query_window, height=10, width=50)
        self.text_query.pack(pady=5)

        self.button_execute = tk.Button(self.query_window, text="Execute", command=self.execute_query)
        self.button_execute.pack(pady=5)

    def open_function1_window(self):
        Function1Window(self.root, self)

    def execute_query(self):
        query = self.text_query.get("1.0", tk.END).strip()

        if not query:
            messagebox.showwarning("Warning", "SQL query cannot be empty.")
            return

        try:
            connection = self.sql_login.connection  # Use the sql_login instance
            if connection is None:
                raise cx_Oracle.InterfaceError("not connected")

            cursor = connection.cursor()
            cursor.execute(query)

            if cursor.description:  # Check if the query returns results
                self.columns = [desc[0] for desc in cursor.description]
                self.rows = cursor.fetchall()
                self.current_page = 0

                # Clear the existing treeview
                for col in self.tree.get_children():
                    self.tree.delete(col)

                # Set the column headers
                self.tree["columns"] = self.columns
                self.tree["show"] = "headings"  # Hide the first empty column
                for col in self.columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, anchor="center")

                self.load_next_page()
            else:
                connection.commit()
                messagebox.showinfo("Success", "Query executed successfully without result.")

            cursor.close()
            self.query_window.destroy()
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error executing query: {e}")
        except cx_Oracle.InterfaceError as e:
            messagebox.showerror("Connection Error", "No active database connection. Please log in again.")

    def load_next_page(self):
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        next_rows = self.rows[start_index:end_index]

        for row in next_rows:
            self.tree.insert("", "end", values=row)

        self.current_page += 1

    def on_tree_configure(self, event):
        if self.tree.yview()[1] > 0.9 and self.current_page * self.page_size < len(self.rows):
            self.load_next_page()

    def back_to_login(self):
        # Close the SQL connection
        if self.sql_login.connection is not None:
            self.sql_login.connection.close()
            self.sql_login.connection = None
            print ("close connect")

        self.frame.pack_forget()
        self.login_app.show_login_screen()

        # 添加 on_closing 方法
    def on_closing(self):
        if self.sql_login.connection is not None:
            self.sql_login.connection.close()
            self.sql_login.connection = None
            print ("close connect")
        self.root.destroy()
