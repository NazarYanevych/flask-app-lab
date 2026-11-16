import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_CONFIG", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_bp
    from .users import users
    from .products import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users)
    app.register_blueprint(products_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="404"), 404

    return app