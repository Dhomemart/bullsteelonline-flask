from flask import Blueprint, render_template, request
import pymysql
import math

product_bp = Blueprint("product", __name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3309,
        user="root",
        password="400364",
        database="metalsheet5"
    )

@product_bp.route("/product")
def show_product():
    keyword = request.args.get("q", "")
    gcode = request.args.get("gcode", "")
    page = int(request.args.get("page", 1))
    per_page = 20

    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        # ดึง gcode และชื่อจากตาราง Productgroup
        cur.execute("SELECT code, name FROM Productgroup ORDER BY code")
        gcodes = cur.fetchall()

        # เงื่อนไขการแสดงผลสินค้า
        sql = """SELECT gcode, id, code, name, qty, unit 
                 FROM product WHERE qty >= 1"""
        count_sql = "SELECT COUNT(*) FROM product WHERE qty >= 1"
        params = []

        if gcode:
            sql += " AND gcode = %s"
            count_sql += " AND gcode = %s"
            params.append(gcode)

        if keyword:
            sql += " AND name LIKE %s"
            count_sql += " AND name LIKE %s"
            params.append("%%" + keyword + "%%")

        sql += " ORDER BY name ASC"

        cur.execute(count_sql, tuple(params))
        total = cur.fetchone()['COUNT(*)']
        total_pages = math.ceil(total / per_page)
        offset = (page - 1) * per_page

        sql += " LIMIT %s OFFSET %s"
        params += [per_page, offset]

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        columns = ["gcode", "id", "code", "name", "qty", "unit"]

    conn.close()
    return render_template("product.html",
        data=rows,
        columns=columns,
        keyword=keyword,
        gcodes=gcodes,
        selected_gcode=gcode,
        page=page,
        total_pages=total_pages
    )
