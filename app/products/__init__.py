from flask import Blueprint

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    template_folder="templates",
    static_folder="static"
)

from . import views
