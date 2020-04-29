from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'search.login'

from app.views import search
app.register_blueprint(search)

# Only required for `flask shell` to play with user/decks database
from app import db
from app.models import User, Deck


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Deck': Deck}
