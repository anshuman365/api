import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog
)

# Define API URL
#API_URL = "https://my-sql-api-service.onrender.com"
API_URL = "http://127.0.0.1:5000"

class DatabaseClient(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_luxury_theme()

    def init_ui(self):
        self.setWindowTitle("PostgreSQL Management System - For Ankit Kumar Srivastava | By Anshuman Singh")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()

        # **Signature Label**
        self.signature_label = QLabel("For Ankit Kumar Srivastava\nBy Anshuman Singh")
        self.signature_label.setStyleSheet("color: #FFD700; font-size: 12px; font-style: italic; text-align: center;")
        layout.addWidget(self.signature_label)

        # **Table Selection**
        table_layout = QHBoxLayout()
        self.table_label = QLabel("Select Table:")
        self.table_dropdown = QComboBox()
        self.fetch_tables_btn = QPushButton("Fetch Tables")
        self.fetch_tables_btn.clicked.connect(self.fetch_tables)

        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_dropdown)
        table_layout.addWidget(self.fetch_tables_btn)
        layout.addLayout(table_layout)

        # **Table Operations**
        operations_layout = QHBoxLayout()
        self.fetch_data_btn = QPushButton("Fetch Data")
        self.insert_data_btn = QPushButton("Insert Data")
        self.update_data_btn = QPushButton("Update Data")
        self.delete_data_btn = QPushButton("Delete Data")
        self.create_table_btn = QPushButton("Create Table")
        self.run_query_btn = QPushButton("Run SQL Query")

        # **Connect Buttons to Functions**
        self.fetch_data_btn.clicked.connect(self.fetch_data)
        self.insert_data_btn.clicked.connect(self.insert_data)
        self.update_data_btn.clicked.connect(self.update_data)
        self.delete_data_btn.clicked.connect(self.delete_data)
        self.create_table_btn.clicked.connect(self.create_table)
        self.run_query_btn.clicked.connect(self.run_custom_query)

        # **Add Buttons to Layout**
        for button in [
            self.fetch_data_btn, self.insert_data_btn, self.update_data_btn,
            self.delete_data_btn, self.create_table_btn, self.run_query_btn
        ]:
            operations_layout.addWidget(button)

        layout.addLayout(operations_layout)

        # **Data Table View**
        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        self.setLayout(layout)

    def apply_luxury_theme(self):
        """Applies a luxury-themed UI."""
        luxury_style = """
        QWidget {
            background-color: #121212;
            color: #E0E0E0;
            font-size: 14px;
            font-family: 'Arial', sans-serif;
        }

        QTableWidget {
            background-color: #1E1E1E;
            border: 2px solid #FFD700;
            color: #E0E0E0;
            gridline-color: #FFD700;
            selection-background-color: #3B3B98;
            selection-color: #FFFFFF;
        }

        QPushButton {
            background-color: #D4AF37;
            color: #000;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 15px;
            border: 2px solid #FFD700;
        }

        QPushButton:hover {
            background-color: #FFD700;
            color: #000;
            border: 2px solid #FFFFFF;
        }

        QComboBox {
            background-color: #222;
            color: #FFD700;
            border: 2px solid #FFD700;
            padding: 5px;
            border-radius: 5px;
        }

        QLabel {
            color: #FFD700;
        }

        QMessageBox {
            background-color: #202020;
            color: #FFD700;
            border: 2px solid #FFD700;
            font-size: 16px;
        }
        """
        self.setStyleSheet(luxury_style)

    def fetch_tables(self):
        """Fetch available tables from the database."""
        try:
            response = requests.get(f"{API_URL}/show_tables")
            result = response.json()

            if result.get("status") == "success":
                tables = result["tables"]
                self.table_dropdown.clear()
                self.table_dropdown.addItems(tables if tables else ["No Tables Available"])
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch tables!")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Network Error: Unable to fetch tables!")

    def fetch_data(self):
        """Fetch data from the selected table."""
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

        try:
            response = requests.post(f"{API_URL}/fetch_data", json={"table_name": table_name})
            result = response.json()

            if result.get("status") == "success":
                data = result["data"]
                if not data:
                    QMessageBox.information(self, "Info", "No data found in this table!")
                    return

                # Set table headers
                columns = list(data[0].keys())
                self.data_table.setColumnCount(len(columns))
                self.data_table.setRowCount(len(data))
                self.data_table.setHorizontalHeaderLabels(columns)

                # Populate table
                for row_idx, row_data in enumerate(data):
                    for col_idx, col_name in enumerate(columns):
                        self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data[col_name])))

            else:
                QMessageBox.critical(self, "Error", "Failed to fetch data!")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Network Error: Unable to fetch data!")
    def create_table(self):
        table_name, ok = QInputDialog.getText(self, "Create Table", "Enter table name:")
        if not ok or not table_name.strip():
            return

        columns, ok = QInputDialog.getMultiLineText(self, "Create Table", 
            "Enter column definitions (e.g., id INT PRIMARY KEY, name TEXT, age INT):\n"
            "Example:\n"
            "id INT PRIMARY KEY,\n"
            "name TEXT,\n"
            "age INT"
        )
        if not ok or not columns.strip():
            return

        response = requests.post(f"{API_URL}/create_table", json={
            "table_name": table_name.strip(),
            "columns": columns.strip()
        })

        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Table creation response"))

    def insert_data(self):
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

    # Get column names
        columns, ok = QInputDialog.getText(self, "Insert Data", "Enter column names (comma-separated):")
        if not ok or not columns.strip():
            return
    
    # Get values
        values, ok = QInputDialog.getText(self, "Insert Data", "Enter values (comma-separated):")
        if not ok or not values.strip():
            return

    # Ensure values are split correctly
        column_list = [col.strip() for col in columns.split(",")]
        value_list = [val.strip() for val in values.split(",")]

    # Ensure column count matches value count
        if len(column_list) != len(value_list):
            QMessageBox.critical(self, "Error", "Number of columns and values must match!")
            return

        response = requests.post(f"{API_URL}/insert_data", json={
            "table_name": table_name.strip(),
            "columns": column_list,  # Send as list
            "values": value_list  # Send as list
        })
    
        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Insert operation response"))

    def update_data(self):
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

    # Get columns and new values
        set_values, ok = QInputDialog.getText(self, "Update Data", "Enter column=value pairs (comma-separated):")
        if not ok or not set_values.strip():
            QMessageBox.warning(self, "Warning", "You must provide values to update.")
            return

    # Get condition (WHERE clause)
        condition, ok = QInputDialog.getText(self, "Update Data", "Enter condition (e.g., id=1):")
        if not ok or not condition.strip():
            QMessageBox.warning(self, "Warning", "You must provide a condition for the update.")
            return

    # Ensure values are correctly formatted
        set_values_list = [val.strip() for val in set_values.split(",")]

        response = requests.post(f"{API_URL}/update_data", json={
            "table_name": table_name.strip(),
            "set_values": set_values_list,  # Send as list
            "condition": condition.strip()  # Send as string
        })

        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Update operation response"))

    def delete_data(self):
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

        condition, ok = QInputDialog.getText(self, "Delete Data", "Enter WHERE condition (e.g., id=1):")
        if not ok or not condition.strip():
            return

        response = requests.post(f"{API_URL}/delete_data", json={
            "table_name": table_name.strip(),
            "condition": condition.strip()
        })

        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Delete response"))
        
    def run_custom_query(self):
        """Runs a user-defined SQL query securely."""
        query, ok = QInputDialog.getMultiLineText(self, "Run SQL Query", "Enter your SQL query:")
        if not ok or not query.strip():
            return  # Do nothing if user cancels or submits an empty query

    # Ensure query ends with a semicolon
        if not query.strip().endswith(";"):
            query = query.strip() + ";"

    # Validate query type
        if not query.strip().lower().startswith(("select", "desc", "describe")):
            QMessageBox.critical(self, "Error", "Only SELECT and DESCRIBE queries are allowed!")
            return

        try:
            response = requests.post(f"{API_URL}/run_query", json={"query": query.strip()})
            result = response.json()

            if result.get("status") == "success":
                if "data" in result:
                # Display data in table for SELECT queries
                    data = result["data"]
                    if data:
                        columns = list(data[0].keys())
                        self.data_table.setColumnCount(len(columns))
                        self.data_table.setRowCount(len(data))
                        self.data_table.setHorizontalHeaderLabels(columns)

                        for row_idx, row_data in enumerate(data):
                            for col_idx, col_name in enumerate(columns):
                                self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data[col_name])))
                    else:
                        QMessageBox.information(self, "Info", "Query executed successfully but returned no data!")
                elif "table_structure" in result:
                # Display table structure for DESCRIBE queries
                    structure = result["table_structure"]
                    self.data_table.setColumnCount(2)
                    self.data_table.setRowCount(len(structure))
                    self.data_table.setHorizontalHeaderLabels(["Column Name", "Data Type"])

                    for row_idx, (col_name, col_type) in enumerate(structure):
                        self.data_table.setItem(row_idx, 0, QTableWidgetItem(col_name))
                        self.data_table.setItem(row_idx, 1, QTableWidgetItem(col_type))
                else:
                    QMessageBox.information(self, "Info", "Query executed successfully!")
            else:
                QMessageBox.critical(self, "Error", result.get("message", "Query execution failed!"))
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Network Error: Unable to execute query!")


# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = DatabaseClient()
    client.show()
    sys.exit(app.exec())