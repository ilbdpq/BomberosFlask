import sqlite3
from flask import Flask, render_template, url_for, redirect, session, send_from_directory, request, g
import datetime

APP = Flask(__name__)
DATABASE = 'databases/bomberos.db'

def Get_DB():
    DB = getattr(g, '_database', None)

    if DB is None:
        DB = g._database = sqlite3.connect(DATABASE)

    return DB

@APP.teardown_appcontext
def Close_DB(exception):
    DB = getattr(g, '_database', None)

    if DB is not None:
        DB.close()

def Init_DB(reset=False):
    with APP.app_context():
        DB = Get_DB()

        if reset or (DB is None):
            with APP.open_resource('schema.sql', mode='r', encoding='UTF-8') as f:
                DB.cursor().executescript(f.read())

            DB.commit()

with APP.app_context():
    Init_DB(True) # Cambiar a True para reiniciar la base de datos

if __name__ == '__main__':
    APP.config['SECRET_KEY'] = 'bdpq'
    APP.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=30)
    APP.run(debug=True)