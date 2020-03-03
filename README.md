# vtes-db

Vampire the Eternal Struggle (VTES) web card database.

## TODO
* Add library card search

## Installation

### Requirements

* Python 3.7+

### Installation

Below is local installation for self-usage / development only.
For production you should at least:
* setup web-server (e.g. nginx) instead of flask embedded web-server
* change app.config['SECRET_KEY']
* disable FLASK_ENV=development

For POSIX:

    git clone https://github.com/smeea/vtes-db.git
    cd vtes-db
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run
    open http://127.0.0.1:5000/crypt

For Windows (cmd.exe):

    git clone https://github.com/smeea/vtes-db.git
    cd vtes-db
    python -m venv c:\path\to\vted-db\venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt
    set FLASK_APP=app
    set FLASK_ENV=development
    flask run
    open http://127.0.0.1:5000/crypt

### License
MIT
