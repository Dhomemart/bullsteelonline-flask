from flask import Blueprint, render_template, request
import pymysql
import os
import math

product_bp = Blueprint("product", __name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("RAILWAY_HOST"),
        port=int(os.getenv("RAILWAY_PORT", 3306)),
        user=os.getenv("RAILWAY_USER"),
        password=os.getenv("RAILWAY_PASSWORD"),
        database=os.getenv("RAILWAY_DATABASE"),
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

        sql = """SELECT gcode, id, code, name, qty, unit FROM product WHERE qty > 0"""
        count_sql = "SELECT COUNT(*) FROM product WHERE qty > 0"

        params = []
        count_params = []

        if gcode:
            sql += " AND gcode = %s"
            count_sql += " AND gcode = %s"
            params.append(gcode)
            count_params.append(gcode)

        if keyword:
            sql += " AND name LIKE %s"
            count_sql += " AND name LIKE %s"
            params.append(f"%{keyword}%")
            count_params.append(f"%{keyword}%")

        sql += " ORDER BY name LIMIT %s OFFSET %s"
        offset = (page - 1) * per_page
        params.extend([per_page, offset])

        cur.execute(sql, tuple(params))
        products = cur.fetchall()

        cur.execute(count_sql, tuple(count_params))
        total = cur.fetchone()['COUNT(*)']
        total_pages = math.ceil(total / per_page)

    conn.close()
    
    # 🔧 แปลง qty เป็น float เพื่อให้ format {:,.2f} ได้
    for row in products:
        try:
            row["qty"] = float(row["qty"])
        except:
            row["qty"] = 0.0

    return render_template("product.html",
                           data=products,
                           columns=["gcode", "id", "code", "name", "qty", "unit"],
                           keyword=keyword,
                           gcodes=gcodes,
                           selected_gcode=gcode,
                           page=page,
                           total_pages=total_pages)
