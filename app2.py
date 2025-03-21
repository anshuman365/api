from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# PostgreSQL Database Configuration (Replace with your Render PostgreSQL credentials)
DB_HOST = os.getenv("DB_HOST", "dpg-cvap03drie7s7397gd20-a.oregon-postgres.render.com")
DB_NAME = os.getenv("DB_NAME", "fraud_detection_db_yhyu")
DB_USER = os.getenv("DB_USER", "fraud_detection_db_yhyu_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "QpeBJon5SXltjAs2AjkTTARwFzZ1yWFc")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route("/")
def home():
    return render_template("index.html")

# Show all databases (PostgreSQL only allows listing if you have superuser privileges)
@app.route("/show_databases", methods=["GET"])
def show_databases():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = [db[0] for db in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "databases": databases})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Show all tables in the connected database
@app.route("/show_tables", methods=["GET"])
def show_tables():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "tables": tables})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Create a new table
@app.route("/create_table", methods=["POST"])
def create_table():
    data = request.json
    table_name = data.get("table_name")
    columns = data.get("columns")

    if not table_name or not columns:
        return jsonify({"status": "error", "message": "Table name and columns are required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        columns_str = ", ".join(columns)
        cursor.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(columns_str)
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": f"Table '{table_name}' created successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Insert data into a table
@app.route("/insert_data", methods=["POST"])
def insert_data():
    data = request.json
    table_name = data.get("table_name")
    values = data.get("values")

    if not table_name or not values:
        return jsonify({"status": "error", "message": "Table name and values are required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(values))
        query = sql.SQL("INSERT INTO {} VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(placeholders)
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Data inserted successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Fetch data from a table
@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    data = request.json
    table_name = data.get("table_name")

    if not table_name:
        return jsonify({"status": "error", "message": "Table name is required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name)))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        result = [dict(zip(columns, row)) for row in rows]
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Update Data API
@app.route("/update_data", methods=["POST"])
def update_data():
    data = request.json
    table_name = data.get("table_name")
    set_values = data.get("set_values")  # Expected: ["name='John'", "class=12"]
    condition = data.get("condition")  # Expected: "id=1"

    if not table_name or not set_values or not condition:
        return jsonify({"status": "error", "message": "Table name, set values, and condition are required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Constructing SQL query safely
        query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(sql.SQL(item) for item in set_values),  # Convert list to SQL
            sql.SQL(condition)  # Directly inserting condition (ensure it's safe)
        )

        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Data updated successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
        

# Delete data from a table
@app.route("/delete_data", methods=["POST"])
def delete_data():
    data = request.json
    table_name = data.get("table_name")
    condition = data.get("condition")

    if not table_name or not condition:
        return jsonify({"status": "error", "message": "Table name and condition are required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = sql.SQL("DELETE FROM {} WHERE {};").format(
            sql.Identifier(table_name),
            sql.SQL(condition)
        )
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Data deleted successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Count rows in a table
@app.route("/count_rows", methods=["POST"])
def count_rows():
    data = request.json
    table_name = data.get("table_name")

    if not table_name:
        return jsonify({"status": "error", "message": "Table name is required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {};").format(sql.Identifier(table_name)))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "row_count": count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Describe a table
@app.route("/describe_table", methods=["POST"])
def describe_table():
    data = request.json
    table_name = data.get("table_name")

    if not table_name:
        return jsonify({"status": "error", "message": "Table name is required"})

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = {};").format(sql.Literal(table_name)))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "table_structure": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/run_query", methods=["POST"])
def run_query():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"status": "error", "message": "SQL query is required"}), 400

    # Only allow SELECT queries for security reasons
    if not query.strip().lower().startswith("select"):
        return jsonify({"status": "error", "message": "Only SELECT queries are allowed"}), 403

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        result = [dict(zip(columns, row)) for row in rows]
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)