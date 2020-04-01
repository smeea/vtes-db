from flask import Flask
from app.views import search

app = Flask(__name__)

# SECRET_KEY is used for cookie session signature, it is not used for anything
# yet, so you can leave it unmodified (it is not security breach).
# Or just change it to some random string.
app.config['SECRET_KEY'] = 'mysecretkey1234567890'

app.register_blueprint(search)
