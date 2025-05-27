from flask import Blueprint, render_template
import pymysql

dashboard_bp = Blueprint("dashboard", __name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3309,
        user="root",
        password="400364",
        database="metalsheet5"
    )

@dashboard_bp.route("/dashboard")
def dashboard():
    stats = {}
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]
        for t in tables:
            cur.execute(f"SELECT COUNT(*) FROM `{t}`")
            stats[t] = cur.fetchone()[0]
    conn.close()
    return render_template("dashboard.html", stats=stats)
