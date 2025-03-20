import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests

API_URL = "http://127.0.0.1:5000"

root = tk.Tk()
root.title("MySQL Client")

frame = tk.Frame(root)
frame.pack(pady=10)

tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

def show_databases():
    response = requests.get(API_URL + "/show_databases")
    result = response.json()
    if result.get("status") == "success":
        messagebox.showinfo("Databases", "\n".join(result["databases"]))
    else:
        messagebox.showerror("Error", result.get("message", "Unknown error"))

def create_database():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    if db_name:
        response = requests.post(API_URL + "/create_database", json={"db_name": db_name})
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def delete_database():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name to Delete:")
    if db_name:
        response = requests.post(API_URL + "/delete_database", json={"db_name": db_name})
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def show_tables():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    if db_name:
        response = requests.post(API_URL + "/show_tables", json={"db_name": db_name})
        result = response.json()
        if result.get("status") == "success":
            messagebox.showinfo("Tables", "\n".join(result["tables"]))
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

def create_table():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    columns = simpledialog.askstring("Columns", "Enter columns (e.g., id INT, name VARCHAR(255)):")
    if db_name and table_name and columns:
        response = requests.post(API_URL + "/create_table", json={
            "db_name": db_name, "table_name": table_name, "columns": columns.split(",")
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def delete_table():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name to Delete:")
    if db_name and table_name:
        response = requests.post(API_URL + "/delete_table", json={"db_name": db_name, "table_name": table_name})
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def insert_data():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    values = simpledialog.askstring("Values", "Enter values (comma-separated):")
    if db_name and table_name and values:
        response = requests.post(API_URL + "/insert_data", json={
            "db_name": db_name, "table_name": table_name, "values": values.split(",")
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def fetch_data():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if db_name and table_name:
        response = requests.post(API_URL + "/fetch_data", json={"db_name": db_name, "table_name": table_name})
        result = response.json()
        if result.get("status") == "success":
            data = result.get("data", [])
            if not data:
                messagebox.showinfo("Info", "No data found.")
                return

            for i in tree.get_children():
                tree.delete(i)

            columns = [f"Col{i}" for i in range(len(data[0]))]
            tree["columns"] = columns
            tree["show"] = "headings"

            for col in columns:
                tree.heading(col, text=col)

            for row in data:
                tree.insert("", "end", values=row)
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

def update_data():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    set_values = simpledialog.askstring("Update Values", "Enter column=value format (e.g., name='John')")
    condition = simpledialog.askstring("Condition", "Enter condition (e.g., id=1)")
    if db_name and table_name and set_values and condition:
        response = requests.post(API_URL + "/update_data", json={
            "db_name": db_name, "table_name": table_name, "set_values": set_values, "condition": condition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def delete_data():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    condition = simpledialog.askstring("Condition", "Enter condition (e.g., id=1)")
    if db_name and table_name and condition:
        response = requests.post(API_URL + "/delete_data", json={
            "db_name": db_name, "table_name": table_name, "condition": condition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def alter_table():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    column_definition = simpledialog.askstring("Column Definition", "Enter column definition (e.g., age INT)")
    if db_name and table_name and column_definition:
        response = requests.post(API_URL + "/alter_table", json={
            "db_name": db_name, "table_name": table_name, "column_definition": column_definition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def drop_column():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    column_name = simpledialog.askstring("Column Name", "Enter Column Name to Drop:")
    if db_name and table_name and column_name:
        response = requests.post(API_URL + "/drop_column", json={
            "db_name": db_name, "table_name": table_name, "column_name": column_name
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def count_rows():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if db_name and table_name:
        response = requests.post(API_URL + "/count_rows", json={"db_name": db_name, "table_name": table_name})
        messagebox.showinfo("Info", f"Row count: {response.json().get('row_count', 'Unknown')}")

def describe_table():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if db_name and table_name:
        response = requests.post(API_URL + "/describe_table", json={"db_name": db_name, "table_name": table_name})
        result = response.json()
        if result.get("status") == "success":
            messagebox.showinfo("Table Structure", str(result["table_structure"]))
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

tk.Button(frame, text="Show Databases", command=show_databases).pack(side=tk.LEFT)
tk.Button(frame, text="Create Database", command=create_database).pack(side=tk.LEFT)
tk.Button(frame, text="Delete Database", command=delete_database).pack(side=tk.LEFT)
tk.Button(frame, text="Show Tables", command=show_tables).pack(side=tk.LEFT)

root.mainloop()