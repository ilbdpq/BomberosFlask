import sqlite3
import click
from flask import g, current_app as APP

DATABASE = 'databases/bomberos.db'

def Get_DB():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def Close_DB(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def Init_DB(reset=False):
    DB = Get_DB()

    if reset or (DB is None):
        with APP.open_resource('schema.sql', mode='r', encoding='UTF-8') as f:
            DB.cursor().executescript(f.read())

        DB.commit()

@click.command('init-db')
def Init_DB_Command():
    '''Inicializa la base de datos.'''
    
    Init_DB(True) # Forzar reinicio de la base de datos
    
    click.echo('Base de datos inicializada.')

def Init_APP(app):
    app.teardown_appcontext(Close_DB)
    app.cli.add_command(Init_DB_Command)