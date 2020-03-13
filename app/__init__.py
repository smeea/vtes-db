from flask import Flask
from app.views import search

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey1234567890'

app.register_blueprint(search)
