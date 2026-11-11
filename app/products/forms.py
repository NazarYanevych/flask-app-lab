from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField("Назва товару", validators=[
        DataRequired(),
        Length(min=3)
    ])

    content = TextAreaField("Опис", validators=[
        DataRequired()
    ], render_kw={"rows": 5, "cols": 40})

    price = DecimalField("Ціна", places=2, validators=[
        InputRequired(),
        NumberRange(min=0.01)
    ], render_kw={"step": "0.01"})

    category = SelectField("Категорія", choices=[
        ("electronics", "Електроніка"),
        ("clothing", "Одяг"),
        ("books", "Книги")
    ])

    quantity = IntegerField("Кількість", validators=[
        InputRequired(),
        NumberRange(min=0)
    ])

    image = FileField("Зображення", validators=[
        FileAllowed(["jpg", "jpeg", "png"], "Дозволені лише JPG та PNG"),
        FileSize(max_size=2 * 1024 * 1024, message="Максимальний розмір — 2 МБ")
    ])

    submit = SubmitField("Зберегти товар")
