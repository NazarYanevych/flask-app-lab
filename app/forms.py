from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[
        DataRequired(),
        Length(min=4, max=10)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    phone = StringField("Телефон", validators=[
        Regexp(r"^\+380\d{9}$", message="Формат: +380...")
    ])
    subject = SelectField("Тема", choices=[
        ("question", "Питання"),
        ("suggestion", "Пропозиція")
    ])

    message = TextAreaField("Повідомлення", validators=[
        DataRequired(),
        Length(max=5000)
    ])

    submit = SubmitField("Надіслати")
