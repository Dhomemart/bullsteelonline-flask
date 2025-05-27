from flask import Flask, render_template, session, redirect, url_for
from routes.product import product_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecret"
app.register_blueprint(product_bp)

start_time = datetime.now()

@app.route("/")
def index():
    return redirect(url_for("product.show_product"))

@app.route("/status")
def status():
    uptime = datetime.now() - start_time
    return f"✅ Flask is running.<br>🕒 Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}<br>⏱ Uptime: {str(uptime).split('.')[0]}"

if __name__ == "__main__":
    with open("flask_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] Flask started\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
