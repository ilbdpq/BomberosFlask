import sqlite3
from flask import Flask
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
import datetime

APP = Flask(__name__)

def Create_APP():
    APP.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='databases/bomberos.db',
        PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=7)
    )

    from scripts import db
    db.Init_APP(APP)

    from scripts import index
    APP.register_blueprint(index.bp)

    return APP

if __name__ == '__main__':
    app = Create_APP()
    app.run(debug=True)