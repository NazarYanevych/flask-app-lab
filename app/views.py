from flask import render_template, request
from app import app


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    return render_template("contacts.html", title="Контакти")


@app.route("/homepage")
def home():
    agent = request.user_agent.string
    return render_template("homepage.html", title="Головна сторінка", agent=agent)