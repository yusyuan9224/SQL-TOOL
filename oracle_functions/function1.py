import tkinter as tk
from tkinter import messagebox
import cx_Oracle

class Function1Window:
    def __init__(self, parent, login_app):
        self.parent = parent
        self.login_app = login_app
        self.function1_window = tk.Toplevel(self.parent)
        self.function1_window.title("Function 1")

        # Add Com ID entry
        self.label_com_id = tk.Label(self.function1_window, text="Com ID:")
        self.label_com_id.pack(pady=5)

        self.entry_com_id = tk.Entry(self.function1_window)
        self.entry_com_id.pack(pady=5)

        # Add ERP ID entry
        self.label_erp_id = tk.Label(self.function1_window, text="ERP ID:")
        self.label_erp_id.pack(pady=5)

        self.entry_erp_id = tk.Entry(self.function1_window)
        self.entry_erp_id.pack(pady=5)

        self.button_confirm = tk.Button(self.function1_window, text="Confirm", command=self.execute_function1)
        self.button_confirm.pack(pady=5)

    def execute_function1(self):
        com_id = self.entry_com_id.get().strip()
        erp_id = self.entry_erp_id.get().strip()

        if not com_id or not erp_id:
            messagebox.showwarning("Warning", "Com ID and ERP ID cannot be empty.")
            return

        query = f"SELECT INA01, INAPOS FROM {com_id}.INA_FILE WHERE INA01 = '{erp_id}'"

        try:
            connection = self.login_app.sql_login.connection  # Use login_app to access sql_login
            if connection is None:
                raise cx_Oracle.InterfaceError("not connected")

            cursor = connection.cursor()
            cursor.execute(query)

            if cursor.description:  # Check if the query returns results
                columns = ["ERP ID (INA01)", "Status (INAPOS)"]
                rows = cursor.fetchall()

                if rows:
                    # Clear the existing treeview
                    for col in self.login_app.tree.get_children():
                        self.login_app.tree.delete(col)

                    # Set the column headers
                    self.login_app.tree["columns"] = columns
                    self.login_app.tree["show"] = "headings"  # Hide the first empty column
                    for col in columns:
                        self.login_app.tree.heading(col, text=col)
                        self.login_app.tree.column(col, anchor="center")

                    for row in rows:
                        self.login_app.tree.insert("", "end", values=row)

                    self.login_app.tree.pack(pady=20, fill=tk.BOTH, expand=True)

                    # Ask if user wants to change status
                    self.ask_change_status(com_id, erp_id)
                else:
                    messagebox.showinfo("No Results", "No data found.")

            else:
                connection.commit()
                messagebox.showinfo("Success", "Query executed successfully without result.")

            cursor.close()
            self.function1_window.destroy()
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error executing query: {e}")
        except cx_Oracle.InterfaceError as e:
            messagebox.showerror("Connection Error", "No active database connection. Please log in again.")

    def ask_change_status(self, com_id, erp_id):
        self.ask_window = tk.Toplevel(self.parent)
        self.ask_window.title("Change Status")

        label = tk.Label(self.ask_window, text="Do you want to change status?")
        label.pack(pady=10)

        button_yes = tk.Button(self.ask_window, text="Yes", command=lambda: self.open_status_window(com_id, erp_id))
        button_yes.pack(side=tk.LEFT, padx=10, pady=10)

        button_no = tk.Button(self.ask_window, text="No", command=self.ask_window.destroy)
        button_no.pack(side=tk.LEFT, padx=10, pady=10)

    def open_status_window(self, com_id, erp_id):
        self.ask_window.destroy()
        self.status_window = tk.Toplevel(self.parent)
        self.status_window.title("Enter New Status")

        label = tk.Label(self.status_window, text="Enter new status (only '3', '1', 'N' allowed):")
        label.pack(pady=10)

        self.entry_status = tk.Entry(self.status_window)
        self.entry_status.pack(pady=10)

        button_confirm = tk.Button(self.status_window, text="Confirm", command=lambda: self.confirm_status_change(com_id, erp_id))
        button_confirm.pack(pady=10)

    def confirm_status_change(self, com_id, erp_id):
        status = self.entry_status.get().strip()

        if status not in ['3', '1', 'N']:
            messagebox.showwarning("Warning", "Invalid status. Only '3', '1', 'N' are allowed.")
            return

        self.status_window.destroy()

        self.confirm_window = tk.Toplevel(self.parent)
        self.confirm_window.title("Confirm Change")

        label = tk.Label(self.confirm_window, text=f"Are you sure you want to change the status to {status}?")
        label.pack(pady=10)

        button_yes = tk.Button(self.confirm_window, text="Yes", command=lambda: self.update_status(com_id, erp_id, status))
        button_yes.pack(side=tk.LEFT, padx=10, pady=10)

        button_no = tk.Button(self.confirm_window, text="No", command=self.confirm_window.destroy)
        button_no.pack(side=tk.LEFT, padx=10, pady=10)

    def update_status(self, com_id, erp_id, status):
        query = f"UPDATE {com_id}.INA_FILE SET INAPOS = :status WHERE INA01 = :erp_id"

        try:
            connection = self.login_app.sql_login.connection  # Use login_app to access sql_login
            if connection is None:
                raise cx_Oracle.InterfaceError("not connected")

            cursor = connection.cursor()
            cursor.execute(query, status=status, erp_id=erp_id)
            connection.commit()

            cursor.close()
            self.confirm_window.destroy()
            messagebox.showinfo("Success", "Status updated successfully.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error updating status: {e}")
        except cx_Oracle.InterfaceError as e:
            messagebox.showerror("Connection Error", "No active database connection. Please log in again.")
