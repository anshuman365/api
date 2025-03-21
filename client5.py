import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog, QTextEdit
)

# Define API URL
API_URL = "https://my-sql-api-service.onrender.com"


class DatabaseClient(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PostgreSQL Management System")
        self.setGeometry(100, 100, 1000, 600)
        
        layout = QVBoxLayout()

        # ** Table Selection **
        self.table_label = QLabel("Select Table:")
        self.table_dropdown = QComboBox()
        self.fetch_tables_btn = QPushButton("Fetch Tables")
        self.fetch_tables_btn.clicked.connect(self.fetch_tables)

        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_dropdown)
        table_layout.addWidget(self.fetch_tables_btn)

        layout.addLayout(table_layout)

        # ** Table Operations **
        self.fetch_data_btn = QPushButton("Fetch Data")
        self.insert_data_btn = QPushButton("Insert Data")
        self.update_data_btn = QPushButton("Update Data")
        self.delete_data_btn = QPushButton("Delete Data")
        self.create_table_btn = QPushButton("Create Table")
        self.run_query_btn = QPushButton("Run SQL Query")

        self.fetch_data_btn.clicked.connect(self.fetch_data)
        self.insert_data_btn.clicked.connect(self.insert_data)
        self.update_data_btn.clicked.connect(self.update_data)
        self.delete_data_btn.clicked.connect(self.delete_data)
        self.create_table_btn.clicked.connect(self.create_table)
        self.run_query_btn.clicked.connect(self.run_custom_query)

        operations_layout = QHBoxLayout()
        operations_layout.addWidget(self.fetch_data_btn)
        operations_layout.addWidget(self.insert_data_btn)
        operations_layout.addWidget(self.update_data_btn)
        operations_layout.addWidget(self.delete_data_btn)
        operations_layout.addWidget(self.create_table_btn)
        operations_layout.addWidget(self.run_query_btn)

        layout.addLayout(operations_layout)

        # ** Data Table View **
        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        self.setLayout(layout)

    def fetch_tables(self):
        response = requests.get(f"{API_URL}/show_tables")
        result = response.json()

        if result.get("status") == "success":
            tables = result["tables"]
            self.table_dropdown.clear()
            self.table_dropdown.addItems(tables if tables else ["No Tables Available"])
        else:
            QMessageBox.critical(self, "Error", "Failed to fetch tables!")

    def fetch_data(self):
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

        response = requests.post(f"{API_URL}/fetch_data", json={"table_name": table_name})
        result = response.json()

        if result.get("status") == "success":
            data = result["data"]
            if not data:
                QMessageBox.information(self, "Info", "No data found in this table!")
                return

            columns = list(data[0].keys())
            self.data_table.setColumnCount(len(columns))
            self.data_table.setRowCount(len(data))
            self.data_table.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(data):
                for col_idx, col_name in enumerate(columns):
                    self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data[col_name])))

        else:
            QMessageBox.critical(self, "Error", "Failed to fetch data!")

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

        columns, ok = QInputDialog.getText(self, "Insert Data", "Enter column names (comma-separated):")
        if not ok or not columns.strip():
            return

        values, ok = QInputDialog.getText(self, "Insert Data", "Enter values (comma-separated):")
        if not ok or not values.strip():
            return

        response = requests.post(f"{API_URL}/insert_data", json={
            "table_name": table_name.strip(),
            "columns": columns.strip(),
            "values": values.strip()
        })
        
        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Insert operation response"))

    def update_data(self):
        table_name = self.table_dropdown.currentText()
        if table_name == "No Tables Available":
            QMessageBox.warning(self, "Warning", "Select a valid table!")
            return

        set_clause, ok = QInputDialog.getText(self, "Update Data", "Enter SET clause (e.g., name='John'):")
        if not ok or not set_clause.strip():
            return

        condition, ok = QInputDialog.getText(self, "Update Data", "Enter WHERE condition (e.g., id=1):")
        if not ok or not condition.strip():
            return

        response = requests.post(f"{API_URL}/update_data", json={
            "table_name": table_name.strip(),
            "set_clause": set_clause.strip(),
            "condition": condition.strip()
        })
        
        result = response.json()
        QMessageBox.information(self, "Result", result.get("message", "Update response"))

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
        query, ok = QInputDialog.getMultiLineText(self, "Run SQL Query", "Enter your SQL query:")
    
        if not ok or not query.strip():
            return  # Do nothing if user cancels or submits an empty query

    # **Only allow SELECT queries**
        if not query.strip().lower().startswith("select"):
            QMessageBox.critical(self, "Error", "Only SELECT queries are allowed!")
            return

        try:
            response = requests.post(f"{API_URL}/run_query", json={"query": query.strip()})
        
        # **Check if the response is valid**
            if response.status_code != 200 or not response.text.strip():
                QMessageBox.critical(self, "Error", "Invalid response from the server!")
                return

            try:
                result = response.json()  # Attempt to parse JSON
            except requests.exceptions.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Invalid JSON response from server!")
                return

            if result.get("status") == "success":
                data = result.get("data", [])

                if not data:
                    QMessageBox.information(self, "Info", "Query executed successfully, but no data returned.")
                    return

            # **Set up table columns**
                columns = list(data[0].keys())
                self.data_table.setColumnCount(len(columns))
                self.data_table.setRowCount(len(data))
                self.data_table.setHorizontalHeaderLabels(columns)

            # **Insert data into table**
                for row_idx, row_data in enumerate(data):
                    for col_idx, col_name in enumerate(columns):
                        self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data[col_name])))
            else:
                QMessageBox.critical(self, "Error", result.get("message", "Query execution failed!"))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network Error: {e}")

# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = DatabaseClient()
    client.show()
    sys.exit(app.exec())