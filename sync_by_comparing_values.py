import pymysql
import os
import datetime
from dotenv import load_dotenv

load_dotenv()  # 🔴 โหลดค่าตัวแปรจากไฟล์ .env

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

# ✅ เชื่อมต่อ Jigsaw (ต้นทาง)
jigsaw_conn = connect_db(
    os.getenv("JIGSAW_HOST"),
    os.getenv("JIGSAW_USER"),
    os.getenv("JIGSAW_PASSWORD"),
    os.getenv("JIGSAW_DATABASE"),
    os.getenv("JIGSAW_PORT")
)

# ✅ เชื่อมต่อ Railway (ปลายทาง)
railway_conn = connect_db(
    os.getenv("RAILWAY_HOST"),
    os.getenv("RAILWAY_USER"),
    os.getenv("RAILWAY_PASSWORD"),
    os.getenv("RAILWAY_DATABASE"),
    os.getenv("RAILWAY_PORT")
)

# 🔁 ตารางที่ต้อง sync
sync_tables = ["productgroup", "product"]

try:
    with jigsaw_conn.cursor() as j_cur, railway_conn.cursor() as r_cur:
        for table in sync_tables:
            j_cur.execute(f"SELECT * FROM {table}")
            jigsaw_rows = j_cur.fetchall()

            insert_count = 0
            update_count = 0

            for row in jigsaw_rows:
                pk = row["id"]
                r_cur.execute(f"SELECT * FROM {table} WHERE id = %s", (pk,))
                existing = r_cur.fetchone()

                if existing:
                    # เปรียบเทียบค่าทุกคอลัมน์ ยกเว้น updated_at
                    changed = any(row[k] != existing.get(k) for k in row if k != "id")
                    if changed:
                        columns = ", ".join([f"{k}=%s" for k in row if k != "id"] + ["updated_at=%s"])
                        values = [row[k] for k in row if k != "id"] + [datetime.datetime.now(), pk]
                        r_cur.execute(f"UPDATE {table} SET {columns} WHERE id = %s", values)
                        update_count += 1
                else:
                    # INSERT ใหม่ พร้อม updated_at
                    row["updated_at"] = datetime.datetime.now()
                    columns = ", ".join(row.keys())
                    placeholders = ", ".join(["%s"] * len(row))
                    r_cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(row.values()))
                    insert_count += 1

            print(f"✅ {table}: เพิ่ม {insert_count} แถว, อัปเดต {update_count} แถว")

        railway_conn.commit()

        # เขียน log
        with open("sync_log.txt", "a", encoding="utf-8") as log:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{now}] ✅ Sync สำเร็จ (เปรียบเทียบค่า)\n")

except Exception as e:
    print("❌ ERROR:", e)
    with open("sync_log.txt", "a", encoding="utf-8") as log:
        log.write(f"[ERROR] {str(e)}\n")

finally:
    jigsaw_conn.close()
    railway_conn.close()
