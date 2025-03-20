function showDatabases() {
    fetch("/show_databases")
        .then(response => response.json())
        .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function createDatabase() {
    const dbName = document.getElementById("db_name").value;
    fetch("/create_database", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({db_name: dbName})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function showTables() {
    fetch("/show_tables")
        .then(response => response.json())
        .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function createTable() {
    const dbName = document.getElementById("db_name_create_table").value;
    const tableName = document.getElementById("table_name").value;
    const columns = document.getElementById("columns").value.split(",");

    fetch("/create_table", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({db_name: dbName, table_name: tableName, columns: columns})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function insertData() {
    const tableName = document.getElementById("insert_table").value;
    const values = document.getElementById("values").value.split(",");

    fetch("/insert_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName, values: values})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function fetchData() {
    const tableName = document.getElementById("fetch_table").value;

    fetch("/fetch_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function updateData() {
    const tableName = document.getElementById("update_table").value;
    const setValues = document.getElementById("set_values").value;
    const condition = document.getElementById("condition_update").value;

    fetch("/update_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName, set_values: setValues, condition: condition})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function deleteData() {
    const tableName = document.getElementById("delete_table").value;
    const condition = document.getElementById("condition_delete").value;

    fetch("/delete_data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName, condition: condition})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function countRows() {
    const tableName = document.getElementById("count_table").value;

    fetch("/count_rows", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}

function describeTable() {
    const tableName = document.getElementById("describe_table").value;

    fetch("/describe_table", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({table_name: tableName})
    })
    .then(response => response.json())
    .then(data => document.getElementById("output").innerText = JSON.stringify(data, null, 2));
}