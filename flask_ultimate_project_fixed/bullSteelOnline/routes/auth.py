from flask import Blueprint, render_template, request, redirect, session, url_for

auth_bp = Blueprint("auth", __name__)

USERS = {
    "admin": "1234",
    "user": "0000"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u, p = request.form["username"], request.form["password"]
        if u in USERS and USERS[u] == p:
            session["user"] = u
            return redirect(url_for("index"))
        return render_template("login.html", error="❌ เข้าสู่ระบบไม่สำเร็จ")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
