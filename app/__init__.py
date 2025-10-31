import sqlite3
import os
import datetime
from flask import Flask
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, send_from_directory
)

APP = Flask(__name__)

def Create_APP():
    APP.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='databases/bomberos.db',
        PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=7)
    )

    from scripts import db
    db.Init_APP(APP)

    from blueprints import bp_index, bp_personal
    APP.register_blueprint(bp_index.bp)
    APP.register_blueprint(bp_personal.bp)

    return APP

@APP.route('/favicon.svg')
def favicon():
    return send_from_directory(os.path.join(APP.root_path, 'static'), 'logo.svg',)

if __name__ == '__main__':
    app = Create_APP()
    
    app.run(
        debug=True,
        host='0.0.0.0',
    )