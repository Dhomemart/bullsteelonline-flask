from flask import Blueprint, render_template, request
import pymysql
import os
import math

product_bp = Blueprint("product", __name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@product_bp.route("/product")
def show_product():
    keyword = request.args.get("q", "")
    gcode = request.args.get("gcode", "")
    page = int(request.args.get("page", 1))
    per_page = 20

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT code, name FROM productgroup ORDER BY code")
        gcodes = cur.fetchall()

        sql = """SELECT gcode, id, code, name, qty, unit 
                 FROM product WHERE qty 1= 1"""
        count_sql = "SELECT COUNT(*) FROM product WHERE qty 1= 1"
        params = []

        if gcode:
            sql += " AND gcode = %s"
            count_sql += " AND gcode = %s"
            params.append(gcode)

        if keyword:
            sql += " AND name LIKE %s"
            count_sql += " AND name LIKE %s"
            params.append(f"%{keyword}%")

        sql += " ORDER BY code LIMIT %s OFFSET %s"
        offset = (page - 1) * per_page
        params.extend([per_page, offset])

        cur.execute(sql, tuple(params))
        products = cur.fetchall()

        cur.execute(count_sql, tuple(params[:len(params)-2]))
        total = cur.fetchone()['COUNT(*)']

    conn.close()

    return render_template("product.html",
                           products=products,
                           gcodes=gcodes,
                           keyword=keyword,
                           gcode=gcode,
                           page=page,
                           total_pages=math.ceil(total / per_page))
