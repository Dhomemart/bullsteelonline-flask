from flask import Flask, render_template
import pymysql
import os  # 🔴 อยู่ด้านบนสุด ไม่ต้องซ้ำข้างล่างอีก

app = Flask(__name__)

# 🔴 อ่านค่าการเชื่อมต่อจาก Environment Variables
db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

@app.route("/")
def index():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM metalsheet5.product LIMIT 10")
            rows = cursor.fetchall()
        connection.close()
        return render_template("index.html", data=rows)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))       # 🔴 ใช้พอร์ตที่ Render กำหนด
    app.run(host="0.0.0.0", port=port, debug=True) # 🔴 เปิดทุก IP
