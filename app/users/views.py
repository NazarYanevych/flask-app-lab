from flask import request, render_template, redirect, url_for, session, flash, make_response
from . import users


@users.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html",
                           name=name, age=age)


@users.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)


@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "secret":
            session["username"] = username
            flash("Вхід виконано успішно", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Неправильний логін або пароль!", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Вхід")



@users.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    cookies = {}
    for key in session.get("cookie_keys", []):
        if key in request.cookies:
            cookies[key] = request.cookies[key]

    return render_template(
        "profile.html",
        username=session["username"],
        cookies=cookies,
        theme=request.cookies.get("theme", "light")
    )



@users.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи", "info")
    return redirect(url_for("users.login"))



@users.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

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
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

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
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    cookie_keys = session.get("cookie_keys", [])

    flash("Усі додані cookies видалено!", "success")
    response = make_response(redirect(url_for("users.profile")))

    for key in cookie_keys:
        response.delete_cookie(key)

    session["cookie_keys"] = []

    return response



@users.route("/set_theme/<theme>")
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    if theme not in ["light", "dark"]:
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 30)

    return response
