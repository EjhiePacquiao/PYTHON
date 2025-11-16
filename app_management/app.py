from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import os
import pathlib
import time
from werkzeug.utils import secure_filename
from sqlite3 import IntegrityError

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
app = Flask(__name__)

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

DB = BASE_DIR / "school.db"

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
PLACEHOLDER = "uploads/placeholder.png"  # relative to static/

# --------------------------------------------------
# DATABASE
# --------------------------------------------------


def get_db_conn():
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db_conn()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idno TEXT UNIQUE NOT NULL,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            course TEXT NOT NULL,
            level TEXT NOT NULL,
            photo TEXT
        )
    """)
    con.commit()
    con.close()


# --------------------------------------------------
# IMAGE HANDLING
# --------------------------------------------------
def allowed_extension(filename):
    return pathlib.Path(filename).suffix.lower() in ALLOWED_EXT


def save_uploaded_image(file_storage, idno):
    """Save uploaded image and return stored filename"""
    if not file_storage or file_storage.filename == "":
        return None

    orig = secure_filename(file_storage.filename)
    ext = pathlib.Path(orig).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError("INVALID_FILE_TYPE")

    filename = f"{idno}_{int(time.time())}{ext}"
    dest = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file_storage.save(dest)

    return filename


def remove_image_file(filename):
    if not filename:
        return
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass


# --------------------------------------------------
# ROUTES
# --------------------------------------------------
@app.route("/")
def index():
    con = get_db_conn()
    cur = con.cursor()
    cur.execute("SELECT * FROM students ORDER BY id DESC")
    students = cur.fetchall()
    con.close()
    return render_template("index.html", students=students)


# --------------------------------------------------
# API: STUDENTS JSON LIST
# --------------------------------------------------
@app.route("/students")
def students_list():
    con = get_db_conn()
    cur = con.cursor()
    cur.execute("SELECT * FROM students ORDER BY id DESC")
    rows = cur.fetchall()
    con.close()

    result = []
    for r in rows:
        filename = r["photo"]
        if filename and os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
            photo_url = url_for(
                "static", filename=f"uploads/{filename}") + f"?v={int(time.time())}"
        else:
            photo_url = url_for("static", filename=PLACEHOLDER)

        result.append({
            "id": r["id"],
            "idno": r["idno"],
            "lastname": r["lastname"],
            "firstname": r["firstname"],
            "course": r["course"],
            "level": r["level"],
            "photo": photo_url
        })

    return jsonify(result)


# --------------------------------------------------
# API: GET SINGLE STUDENT (WITH DEBUG)
# --------------------------------------------------
@app.route("/student/<int:sid>")
def get_student(sid):
    con = get_db_conn()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (sid,))
    row = cur.fetchone()
    con.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    filename = row["photo"]
    print(f"DEBUG - Student ID: {sid}")
    print(f"DEBUG - Filename from DB: {filename}")

    if filename:
        full_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        print(f"DEBUG - Full path: {full_path}")
        print(f"DEBUG - File exists: {os.path.exists(full_path)}")

    if filename and os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
        photo_url = url_for(
            "static", filename=f"uploads/{filename}") + f"?v={int(time.time())}"
    else:
        photo_url = url_for("static", filename=PLACEHOLDER)

    print(f"DEBUG - Photo URL: {photo_url}")

    return jsonify({
        "id": row["id"],
        "idno": row["idno"],
        "lastname": row["lastname"],
        "firstname": row["firstname"],
        "course": row["course"],
        "level": row["level"],
        "photo": photo_url
    })


# --------------------------------------------------
# API: ADD STUDENT
# --------------------------------------------------
@app.route("/add", methods=["POST"])
def add_student():
    idno = request.form.get("idno", "").strip()
    ln = request.form.get("lastname", "").strip()
    fn = request.form.get("firstname", "").strip()
    course = request.form.get("course", "").strip()
    level = request.form.get("level", "").strip()

    if not (idno and ln and fn and course and level):
        return jsonify({"error": "MISSING_FIELDS"}), 400
    # ---------------------------------------------------
    print(f"DEBUG ADD - Form data: {request.form}")
    print(f"DEBUG ADD - Files: {request.files}")

    image_file = request.files.get("image")
    print(f"DEBUG ADD - image_file object: {image_file}")
    print(
        f"DEBUG ADD - image_file.filename: {image_file.filename if image_file else 'NO FILE'}")

    filename = None

    if image_file and image_file.filename:
        print(f"DEBUG ADD - About to save image for idno: {idno}")
        filename = save_uploaded_image(image_file, idno)
        print(f"DEBUG ADD - Saved filename: {filename}")
    else:
        print("DEBUG ADD - No image to save")
# -----------------------------------------------------
    image_file = request.files.get("image")
    filename = None

    if image_file and image_file.filename:
        filename = save_uploaded_image(image_file, idno)

    con = get_db_conn()
    cur = con.cursor()

    try:
        cur.execute("""
            INSERT INTO students (idno, lastname, firstname, course, level, photo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (idno, ln, fn, course, level, filename))
        con.commit()
        new_id = cur.lastrowid
    except IntegrityError:
        con.close()
        remove_image_file(filename)
        return jsonify({"error": "IDNO_EXISTS"}), 409

    con.close()
    return jsonify({"message": "Student added", "id": new_id})


# --------------------------------------------------
# API: UPDATE STUDENT
# --------------------------------------------------
@app.route("/update/<int:sid>", methods=["POST"])
def update_student(sid):
    idno = request.form.get("idno", "").strip()
    ln = request.form.get("lastname", "").strip()
    fn = request.form.get("firstname", "").strip()
    course = request.form.get("course", "").strip()
    level = request.form.get("level", "").strip()

    if not (idno and ln and fn and course and level):
        return jsonify({"error": "MISSING_FIELDS"}), 400

    image_file = request.files.get("image")
    filename = None

    if image_file and image_file.filename:
        filename = save_uploaded_image(image_file, idno)

    con = get_db_conn()
    cur = con.cursor()

    cur.execute("SELECT photo FROM students WHERE id=?", (sid,))
    row = cur.fetchone()

    if not row:
        con.close()
        if filename:
            remove_image_file(filename)
        return jsonify({"error": "NOT_FOUND"}), 404

    old_photo = row["photo"]

    try:
        if filename:
            cur.execute("""
                UPDATE students
                SET idno=?, lastname=?, firstname=?, course=?, level=?, photo=?
                WHERE id=?
            """, (idno, ln, fn, course, level, filename, sid))
        else:
            cur.execute("""
                UPDATE students
                SET idno=?, lastname=?, firstname=?, course=?, level=?
                WHERE id=?
            """, (idno, ln, fn, course, level, sid))

        con.commit()
    except IntegrityError:
        con.close()
        remove_image_file(filename)
        return jsonify({"error": "IDNO_EXISTS"}), 409

    con.close()

    if filename and old_photo:
        remove_image_file(old_photo)

    return jsonify({"message": "Student updated", "id": sid})


# --------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------
@app.route("/delete/<int:sid>", methods=["POST"])
def delete_student(sid):
    con = get_db_conn()
    cur = con.cursor()

    cur.execute("SELECT photo FROM students WHERE id=?", (sid,))
    row = cur.fetchone()

    if not row:
        con.close()
        return jsonify({"error": "NOT_FOUND"}), 404

    old_photo = row["photo"]

    cur.execute("DELETE FROM students WHERE id=?", (sid,))
    con.commit()
    con.close()

    if old_photo:
        remove_image_file(old_photo)

    return jsonify({"message": "Student deleted"})


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
