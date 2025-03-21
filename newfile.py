import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Scrollbar
import requests

API_URL = "https://my-sql-api-service.onrender.com"

root = tk.Tk()
root.title("MySQL Client")
root.geometry("350x500")  # Adjusted for a smaller screen

# Scrollable frame setup
canvas = tk.Canvas(root)
scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

# Configure scrolling
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

# Treeview for displaying tabular data
tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

# Functions (Same as your code, added missing functions)
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

# More functions
def count_rows():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    if db_name and table_name:
        response = requests.post(API_URL + "/count_rows", json={"db_name": db_name, "table_name": table_name})
        messagebox.showinfo("Info", f"Row count: {response.json().get('row_count', 'Unknown')}")

def alter_table():
    db_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    table_name = simpledialog.askstring("Table Name", "Enter Table Name:")
    column_definition = simpledialog.askstring("Column Definition", "Enter column definition (e.g., age INT)")
    if db_name and table_name and column_definition:
        response = requests.post(API_URL + "/alter_table", json={
            "db_name": db_name, "table_name": table_name, "column_definition": column_definition
        })
        messagebox.showinfo("Info", response.json().get("message", "Unknown response"))

# Grid layout for buttons
buttons = [
    ("Show Databases", show_databases),
    ("Create Database", create_database),
    ("Delete Database", delete_database),
    ("Show Tables", show_tables),
    ("Create Table", create_table),
    ("Delete Table", delete_table),
    ("Insert Data", insert_data),
    ("Fetch Data", fetch_data),
    ("Count Rows", count_rows),
    ("Alter Table", alter_table),
]

for i, (text, command) in enumerate(buttons):
    row, col = divmod(i, 2)  # Arrange buttons in 2 columns
    btn = tk.Button(frame, text=text, command=command, width=18, height=2)
    btn.grid(row=row, column=col, padx=5, pady=5)

# Pack UI elements
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

root.mainloop()