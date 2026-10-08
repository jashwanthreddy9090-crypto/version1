from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from openpyxl import Workbook, load_workbook
from datetime import datetime
import sqlite3, os, io, re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "campus-care-dev-secret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "campuscare.db")
LOGIN_EXCEL = os.path.join(BASE_DIR, "Campus360_Login_Data.xlsx")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@campus.360").lower()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Campus360@Admin2026")

def valid_campus_email(email):
    return bool(re.fullmatch(r"[^@\s]+@campus\.360", email.strip().lower()))

def db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student'
    )''')
    row = con.execute("SELECT id FROM users WHERE email=?", (ADMIN_EMAIL,)).fetchone()
    if not row:
        con.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                    ("Campus Administrator", ADMIN_EMAIL,
                     generate_password_hash(ADMIN_PASSWORD), "admin"))
    con.commit()
    con.close()

def log_login(name, email, role, status):
    headers=["Date/Time","Name","Campus Email","Role","Login Status"]
    if os.path.exists(LOGIN_EXCEL):
        wb=load_workbook(LOGIN_EXCEL)
        ws=wb.active
    else:
        wb=Workbook()
        ws=wb.active
        ws.title="Login Data"
        ws.append(headers)
    ws.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               name, email, role, status])
    wb.save(LOGIN_EXCEL)

@app.route("/")
def home():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email=request.form.get("email","").strip().lower()
    password=request.form.get("password","")
    if not valid_campus_email(email):
        flash("Use your official @campus.360 account.")
        return redirect(url_for("home"))
    con=db()
    user=con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    con.close()
    if user and check_password_hash(user["password"], password):
        session["user"]={"id":user["id"],"name":user["name"],
                         "email":user["email"],"role":user["role"]}
        log_login(user["name"],email,user["role"],"SUCCESS")
        return redirect(url_for("dashboard"))
    log_login(user["name"] if user else "Unknown",email,
              user["role"] if user else "unknown","FAILED")
    flash("Invalid credentials.")
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("home"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin/create-student", methods=["POST"])
def create_student():
    if session.get("user",{}).get("role") != "admin":
        return "Unauthorized", 403
    name=request.form.get("name","").strip()
    email=request.form.get("email","").strip().lower()
    password=request.form.get("password","")
    if not name or not valid_campus_email(email) or not password:
        return "Invalid student details", 400
    con=db()
    try:
        con.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                    (name,email,generate_password_hash(password),"student"))
        con.commit()
    except sqlite3.IntegrityError:
        return "Email already exists", 409
    finally:
        con.close()
    return "Student created successfully"

@app.route("/admin/login-data")
def login_data():
    if session.get("user",{}).get("role") != "admin":
        return "Unauthorized", 403
    if not os.path.exists(LOGIN_EXCEL):
        log_login("System","system@campus.360","admin","FILE_CREATED")
    return send_file(LOGIN_EXCEL, as_attachment=True,
                     download_name="Campus360_Login_Data.xlsx")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
