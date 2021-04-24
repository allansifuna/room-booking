from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from bookingapp.config import Config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
lm = LoginManager()
lm.login_view = 'user.login'
lm.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from bookingapp.user.routes import user

    db.init_app(app)
    bcrypt.init_app(app)
    lm.init_app(app)

    app.register_blueprint(user)
    return(app)
