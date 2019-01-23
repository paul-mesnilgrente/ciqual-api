from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api

from config import Config

import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
api_bp = Blueprint('apibp', __name__)
api = Api(api_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    # api.init_app(app)


    from app.api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(api_bp)

    if not app.debug:
        file_handler = RotatingFileHandler('logs/ciqual.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ciqual startup')

    return app

from app import models