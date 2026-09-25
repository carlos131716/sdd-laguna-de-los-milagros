import sqlite3
from functools import wraps

from flask import flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db


def validate_email(email):
    email = email.strip().lower()
    if not email or "@" not in email or len(email) > 254:
        return email, "Ingrese un correo electrónico válido."
    return email, None


def load_logged_in_user(app):
    user_id = session.get("user_id")
    g.user = get_db(app).execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchone() if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)
    return wrapped_view


def register_routes(app):
    @app.route("/registro", methods=("GET", "POST"))
    def register():
        if request.method == "POST":
            email, email_error = validate_email(request.form.get("email", ""))
            password = request.form.get("password", "")
            error = email_error
            if error is None and len(password) < 8:
                error = "La contraseña debe tener al menos 8 caracteres."
            if error is None:
                try:
                    db = get_db(app)
                    db.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, generate_password_hash(password)))
                    db.commit()
                except sqlite3.IntegrityError:
                    error = "Ya existe una cuenta con ese correo."
            if error:
                flash(error, "error")
            else:
                flash("Cuenta creada. Ahora puedes iniciar sesión.", "success")
                return redirect(url_for("login"))
            return render_template("register.html", email=email)
        return render_template("register.html", email="")

    @app.route("/login", methods=("GET", "POST"))
    def login():
        if request.method == "POST":
            email, email_error = validate_email(request.form.get("email", ""))
            user = get_db(app).execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if email_error or user is None or not check_password_hash(user["password_hash"], request.form.get("password", "")):
                flash("Correo o contraseña incorrectos.", "error")
            else:
                session.clear()
                session["user_id"] = user["id"]
                next_url = request.args.get("next") or url_for("index")
                if not next_url.startswith("/") or next_url.startswith("//"):
                    next_url = url_for("index")
                return redirect(next_url)
        return render_template("login.html")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))
