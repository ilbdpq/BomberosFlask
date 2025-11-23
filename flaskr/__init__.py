import sqlite3
import os
import datetime
from flask import Flask
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, send_from_directory
)
from .blueprints.bp_index import Admin_Required, User_Required

def Create_APP():
    APP = Flask(__name__, instance_relative_config=True)
    
    APP.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(APP.instance_path, 'bomberos.db'),
        PERMANENT_SESSION_LIFETIME=datetime.timedelta(minutes=30)
    )

    from .scripts import db
    db.Init_APP(APP)

    from .blueprints import bp_index, bp_personal, bp_unidades, bp_eventos, bp_asistencias, bp_calificaciones, bp_tests
    APP.register_blueprint(bp_index.bp)
    APP.register_blueprint(bp_personal.bp, url_prefix='/personal')
    APP.register_blueprint(bp_unidades.bp, url_prefix='/unidades')
    APP.register_blueprint(bp_eventos.bp, url_prefix='/eventos')
    APP.register_blueprint(bp_asistencias.bp, url_prefix='/asistencias')
    APP.register_blueprint(bp_calificaciones.bp, url_prefix='/calificaciones')
    APP.register_blueprint(bp_tests.bp, url_prefix='/tests')
    
    APP.add_template_global(Admin_Required, 'Admin_Required')
    APP.add_template_global(User_Required, 'User_Required')

    return APP

if __name__ == '__main__':
    app = Create_APP()
    
    app.run(
        debug=True,
        host='0.0.0.0',
    )