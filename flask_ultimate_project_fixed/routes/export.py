from flask import Blueprint, Response
import pymysql

export_bp = Blueprint("export", __name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3309,
        user="root",
        password="400364",
        database="metalsheet5"
    )

@export_bp.route("/export/<table_name>")
def export_csv(table_name):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM `{table_name}`")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    conn.close()

    def generate():
        yield ",".join(columns) + "\n"
        for row in rows:
            yield ",".join(str(r) for r in row) + "\n"

    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={table_name}.csv"})
