from flask import request, render_template, redirect, url_for, session, flash
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
        flash("Спочатку увійдіть у систему", "danger")
        return redirect(url_for("users.login"))

    return render_template(
        "profile.html",
        title="Профіль",
        username=session["username"]
    )


@users.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи", "info")
    return redirect(url_for("users.login"))
