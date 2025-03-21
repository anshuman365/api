import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests

API_URL = "https://my-sql-api-service.onrender.com"

# Initialize the main Tkinter window
root = tk.Tk()
root.title("MySQL Client")

frame = tk.Frame(root)
frame.pack(pady=10)

# Treeview for displaying data
tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

def update_treeview(data):
    """Update treeview with new data."""
    for i in tree.get_children():
        tree.delete(i)

    if not data:
        messagebox.showinfo("Info", "No data found.")
        return

    columns = list(data[0].keys())  # Extract column names dynamically
    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for row in data:
        tree.insert("", "end", values=list(row.values()))

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
            "db_name": db_name,
            "table_name": table_name,
            "columns": columns.split(",")
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def insert_data():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    values = simpledialog.askstring("Values", "Enter values (comma-separated):")
    if table_name and values:
        response = requests.post(API_URL + "/insert_data", json={
            "table_name": table_name,
            "values": values.split(",")
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def fetch_data():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if table_name:
        response = requests.post(API_URL + "/fetch_data", json={"table_name": table_name})
        result = response.json()
        if result.get("status") == "success":
            update_treeview(result.get("data", []))
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

def update_data():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    set_values = simpledialog.askstring("Set Values", "Enter update values (e.g., column='value'):")
    condition = simpledialog.askstring("Condition", "Enter condition (e.g., id=1):")
    if table_name and set_values and condition:
        response = requests.post(API_URL + "/update_data", json={
            "table_name": table_name,
            "set_values": set_values,
            "condition": condition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def delete_data():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    condition = simpledialog.askstring("Condition", "Enter condition (e.g., id=1):")
    if table_name and condition:
        response = requests.post(API_URL + "/delete_data", json={
            "table_name": table_name,
            "condition": condition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

def count_rows():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if table_name:
        response = requests.post(API_URL + "/count_rows", json={"table_name": table_name})
        result = response.json()
        if result.get("status") == "success":
            messagebox.showinfo("Row Count", f"Total rows: {result.get('count', 0)}")
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

def describe_table():
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if table_name:
        response = requests.post(API_URL + "/describe_table", json={"table_name": table_name})
        result = response.json()
        if result.get("status") == "success":
            update_treeview(result.get("description", []))
        else:
            messagebox.showerror("Error", result.get("message", "Unknown error"))

# Buttons for each operation
tk.Button(frame, text="Show Databases", command=show_databases).pack(side="left")
tk.Button(frame, text="Create Database", command=create_database).pack(side="left")
tk.Button(frame, text="Delete Database", command=delete_database).pack(side="left")
tk.Button(frame, text="Show Tables", command=show_tables).pack(side="left")
tk.Button(frame, text="Create Table", command=create_table).pack(side="left")
tk.Button(frame, text="Insert Data", command=insert_data).pack(side="left")
tk.Button(frame, text="Fetch Data", command=fetch_data).pack(side="left")
tk.Button(frame, text="Update Data", command=update_data).pack(side="left")
tk.Button(frame, text="Delete Data", command=delete_data).pack(side="left")
tk.Button(frame, text="Count Rows", command=count_rows).pack(side="left")
tk.Button(frame, text="Describe Table", command=describe_table).pack(side="left")

root.mainloop()