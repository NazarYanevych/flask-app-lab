from pathlib import Path

from flask import Blueprint, render_template, request, redirect, url_for, flash

from .forms import ContactForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        log_file = Path("contacts.log")

        with log_file.open("a", encoding="utf-8") as file:
            file.write(
                f"Ім'я: {form.name.data}, "
                f"Email: {form.email.data}, "
                f"Телефон: {form.phone.data}, "
                f"Тема: {form.subject.data}, "
                f"Повідомлення: {form.message.data}\n"
            )
        flash("Повідомлення успішно надіслано", "success")
        return redirect(url_for("main.contacts"))
    if form.is_submitted():
        flash("Перевірте введені дані", "danger")

    return render_template("contacts.html", title="Контакти", form=form)


@main_bp.route("/homepage")
def home():
    agent = request.user_agent.string
    return render_template("homepage.html", title="Головна сторінка", agent=agent)