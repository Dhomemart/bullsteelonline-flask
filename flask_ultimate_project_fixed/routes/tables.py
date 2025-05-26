from flask import Blueprint, render_template
import pymysql

tables_bp = Blueprint("tables", __name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3309,
        user="root",
        password="400364",
        database="metalsheet5"
    )

@tables_bp.route("/tables")
def list_tables():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]
    conn.close()
    return render_template("tables.html", tables=tables)

@tables_bp.route("/tables/<table_name>")
def view_table(table_name):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM `{table_name}`")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    conn.close()
    return render_template("table_data.html", table_name=table_name, data=rows, columns=columns)
