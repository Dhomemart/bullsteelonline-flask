import pymysql  # 🔴 ไลบรารีเชื่อมต่อ MySQL
import os       # 🔴 สำหรับดึงค่าตัวแปรจากระบบ
import datetime  # 🔴 สำหรับ timestamp
import time      # 🔴 สำหรับจับเวลา
from dotenv import load_dotenv  # 🔴 โหลดค่าตัวแปรจากไฟล์ .env

load_dotenv()  # 🔴 โหลดไฟล์ .env เพื่อใช้ตัวแปรเชื่อมฐานข้อมูล

# 🔧 ฟังก์ชันเชื่อมต่อฐานข้อมูล
def connect_db(host, user, password, database, port):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ Connect to Jigsaw Server (ต้นทาง)
jigsaw_conn = connect_db(
    os.getenv("JIGSAW_HOST"),
    os.getenv("JIGSAW_USER"),
    os.getenv("JIGSAW_PASSWORD"),
    os.getenv("JIGSAW_DATABASE"),
    os.getenv("JIGSAW_PORT")
)

# ✅ Connect to Railway MySQL (ปลายทาง)
railway_conn = connect_db(
    os.getenv("RAILWAY_HOST"),
    os.getenv("RAILWAY_USER"),
    os.getenv("RAILWAY_PASSWORD"),
    os.getenv("RAILWAY_DATABASE"),
    os.getenv("RAILWAY_PORT")
)

try:
    start_time = time.time()  # ⏱ เริ่มจับเวลา

    with jigsaw_conn.cursor() as j_cursor, railway_conn.cursor() as r_cursor:

        # 🔍 หา id ล่าสุดในฝั่ง Railway ก่อน
        r_cursor.execute("SELECT MAX(id) AS last_id FROM product")
        last_id = r_cursor.fetchone()["last_id"] or 0

        # 📤 ดึงข้อมูลใหม่จาก Jigsaw ที่มี id > ล่าสุด
        j_cursor.execute("SELECT * FROM product WHERE id > %s", (last_id,))
        new_rows = j_cursor.fetchall()

        print(f"พบข้อมูลใหม่ {len(new_rows)} รายการที่จะ Sync...")

        # 🔄 Insert ข้อมูลใหม่เข้า Railway
        for row in new_rows:
            columns = ", ".join(row.keys())
            placeholders = ", ".join(["%s"] * len(row))
            values = tuple(row.values())

            sql = f"INSERT INTO product ({columns}) VALUES ({placeholders})"
            r_cursor.execute(sql, values)

        railway_conn.commit()
        print("✅ Sync สำเร็จ")

        # ✅ เขียน log success
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        with open("sync_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{now}] ✅ Sync สำเร็จ {len(new_rows)} รายการ ใช้เวลา {elapsed} วินาที\n")

except Exception as e:
    print("❌ Error:", e)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("sync_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{now}] ❌ ERROR: {str(e)}\n")

finally:
    jigsaw_conn.close()
    railway_conn.close()
