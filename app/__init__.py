from flask import Flask

app = Flask(__name__)

from . import views
from .users import users
from .products import products_bp

app.register_blueprint(users)
app.register_blueprint(products_bp)
