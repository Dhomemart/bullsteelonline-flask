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
    category = request.args.get("gcode", "")
    page = int(request.args.get("page", 1))
    per_page = 10  # จำนวนสินค้าต่อหน้า

    conn = get_connection()
    with conn.cursor() as cur:
        # ดึงประเภทสินค้า
        cur.execute("SELECT DISTINCT gcode FROM product")
        categories = [row[0] for row in cur.fetchall()]

        # ค้นหาสินค้า
        sql = "SELECT * FROM product WHERE 1=1"
        count_sql = "SELECT COUNT(*) FROM product WHERE 1=1"
        params = []

        if keyword:
            sql += " AND name LIKE %s"
            count_sql += " AND name LIKE %s"
            params.append("%%" + keyword + "%%")
        if category:
            sql += " AND gcode = %s"
            count_sql += " AND gcode = %s"
            params.append(category)

        cur.execute(count_sql, tuple(params))
        total = cur.fetchone()[0]
        total_pages = math.ceil(total / per_page)
        offset = (page - 1) * per_page

        sql += " LIMIT %s OFFSET %s"
        params += [per_page, offset]

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

    conn.close()
    return render_template("product.html", data=rows, columns=columns,
                           keyword=keyword, categories=categories,
                           selected_category=category,
                           page=page, total_pages=total_pages)
