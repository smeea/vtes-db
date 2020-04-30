from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'

from app import views

# Everything below only required for `flask shell` to play with database
# from app import db
# from app.models import User, Deck

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Deck': Deck}
