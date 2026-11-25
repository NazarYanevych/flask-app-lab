from flask import request, render_template, redirect, url_for, session, flash, make_response
from flask_login import login_user, login_required, current_user, logout_user

from app import db
from . import users
from .forms import RegistrationForm, LoginForm
from .models import User


@users.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html", name=name, age=age)


@users.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password="",
        )
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Акаунт для {form.username.data} створено! Тепер ви можете увійти.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form, title="Реєстрація")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Вітаю, {user.username}! Вхід успішний.", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("users.account"))
        flash("Неправильний email або пароль!", "danger")

    return render_template("login.html", form=form, title="Вхід")


@users.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user, title="Account")


@users.route("")
@login_required
def all_users():
    users_list = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template("users_list.html", users_list=users_list, title="Users List")


@users.route("/profile")
@login_required
def profile():
    cookies = {}
    for key in session.get("cookie_keys", []):
        if key in request.cookies:
            cookies[key] = request.cookies[key]

    return render_template(
        "profile.html",
        username=current_user.username,
        cookies=cookies,
        theme=request.cookies.get("theme", "light"),
    )


@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи", "info")
    return redirect(url_for("users.login"))


@users.route("/add_cookie", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", type=int)

    if not key or key.lower() in ("session", "cookie_keys") or max_age is None or max_age <= 0:
        flash("Вкажіть коректний ключ і термін дії", "danger")
        return redirect(url_for("users.profile"))

    cookie_keys = session.get("cookie_keys", [])

    if key not in cookie_keys:
        cookie_keys.append(key)

    session["cookie_keys"] = cookie_keys

    flash("Cookie успішно додано", "success")
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)

    return response


@users.route("/delete_cookie", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "")

    cookie_keys = session.get("cookie_keys", [])

    if key not in cookie_keys:
        flash("Cookie не знайдено!", "danger")
        return redirect(url_for("users.profile"))

    cookie_keys.remove(key)
    session["cookie_keys"] = cookie_keys

    flash("Cookie успішно видалено!", "success")
    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)

    return response


@users.route("/delete_all_cookies", methods=["POST"])
@login_required
def delete_all_cookies():
    cookie_keys = session.get("cookie_keys", [])

    flash("Усі додані cookies видалено!", "success")
    response = make_response(redirect(url_for("users.profile")))

    for key in cookie_keys:
        response.delete_cookie(key)

    session["cookie_keys"] = []

    return response


@users.route("/set_theme/<theme>")
@login_required
def set_theme(theme):
    if theme not in ["light", "dark"]:
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 30)

    return response