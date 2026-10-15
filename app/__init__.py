from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "lab4"

from . import views
from .users import users
from .products import products_bp

app.register_blueprint(users)
app.register_blueprint(products_bp)
