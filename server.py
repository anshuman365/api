from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    buffered=True,
    autocommit=True
)
cursor = mydb.cursor()

@app.route('/')
def home():
	return render_template("index.html")
	
# Show all databases
@app.route('/show_databases', methods=['GET'])
def show_databases():
    cursor.execute("SHOW DATABASES;")
    databases = [db[0] for db in cursor.fetchall()]
    return jsonify({"status": "success", "databases": databases})

# Create a new database
@app.route('/create_database', methods=['POST'])
def create_database():
    data = request.json
    db_name = data.get("db_name")
    
    if not db_name:
        return jsonify({"status": "error", "message": "Database name is required"})
    
    cursor.execute(f"CREATE DATABASE {db_name};")
    return jsonify({"status": "success", "message": f"Database '{db_name}' created successfully!"})

# Delete a database
@app.route('/delete_database', methods=['POST'])
def delete_database():
    data = request.json
    db_name = data.get("db_name")

    if not db_name:
        return jsonify({"status": "error", "message": "Database name is required"})

    cursor.execute(f"DROP DATABASE {db_name};")
    return jsonify({"status": "success", "message": f"Database '{db_name}' deleted successfully!"})

# Show all tables in a database
@app.route('/show_tables', methods=['POST'])
def show_tables():
    data = request.json
    db_name = data.get("db_name")

    if not db_name:
        return jsonify({"status": "error", "message": "Database name is required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]
    return jsonify({"status": "success", "tables": tables})

# Create Table
@app.route('/create_table', methods=['POST'])
def create_table():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    columns = data.get("columns")

    if not db_name or not table_name or not columns:
        return jsonify({"status": "error", "message": "Database, table name, and columns are required"})

    cursor.execute(f"USE {db_name};")
    query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    cursor.execute(query)
    return jsonify({"status": "success", "message": f"Table '{table_name}' created successfully!"})

# Delete a table
@app.route('/delete_table', methods=['POST'])
def delete_table():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")

    if not db_name or not table_name:
        return jsonify({"status": "error", "message": "Database and table name are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"DROP TABLE {table_name};")
    return jsonify({"status": "success", "message": f"Table '{table_name}' deleted successfully!"})

# Insert Data
@app.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    values = data.get("values")

    if not db_name or not table_name or not values:
        return jsonify({"status": "error", "message": "Database, table name, and values are required"})

    cursor.execute(f"USE {db_name};")
    placeholders = ', '.join(['%s' for _ in values])
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", values)
    return jsonify({"status": "success", "message": "Data inserted successfully!"})

# Fetch Data
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")

    if not db_name or not table_name:
        return jsonify({"status": "error", "message": "Database and table name are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"SELECT * FROM {table_name};")
    result = cursor.fetchall()
    return jsonify({"status": "success", "data": result})

# Update Data
@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    set_values = data.get("set_values")
    condition = data.get("condition")

    if not db_name or not table_name or not set_values or not condition:
        return jsonify({"status": "error", "message": "Database, table name, set values, and condition are required"})

    cursor.execute(f"USE {db_name};")
    query = f"UPDATE {table_name} SET {set_values} WHERE {condition};"
    cursor.execute(query)
    return jsonify({"status": "success", "message": "Data updated successfully!"})

# Delete Data (Row)
@app.route('/delete_data', methods=['POST'])
def delete_data():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    condition = data.get("condition")

    if not db_name or not table_name or not condition:
        return jsonify({"status": "error", "message": "Database, table name, and condition are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition};")
    return jsonify({"status": "success", "message": "Data deleted successfully!"})

# Alter Table (Add Column)
@app.route('/alter_table', methods=['POST'])
def alter_table():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    column_definition = data.get("column_definition")

    if not db_name or not table_name or not column_definition:
        return jsonify({"status": "error", "message": "Database, table name, and column definition are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_definition};")
    return jsonify({"status": "success", "message": f"Column added to '{table_name}' successfully!"})

# Drop Column from Table
@app.route('/drop_column', methods=['POST'])
def drop_column():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")
    column_name = data.get("column_name")

    if not db_name or not table_name or not column_name:
        return jsonify({"status": "error", "message": "Database, table name, and column name are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")
    return jsonify({"status": "success", "message": f"Column '{column_name}' dropped from '{table_name}' successfully!"})

# Count Rows in Table
@app.route('/count_rows', methods=['POST'])
def count_rows():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")

    if not db_name or not table_name:
        return jsonify({"status": "error", "message": "Database and table name are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    return jsonify({"status": "success", "row_count": count})

# Describe Table
@app.route('/describe_table', methods=['POST'])
def describe_table():
    data = request.json
    db_name = data.get("db_name")
    table_name = data.get("table_name")

    if not db_name or not table_name:
        return jsonify({"status": "error", "message": "Database and table name are required"})

    cursor.execute(f"USE {db_name};")
    cursor.execute(f"DESCRIBE {table_name};")
    result = cursor.fetchall()
    return jsonify({"status": "success", "table_structure": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)