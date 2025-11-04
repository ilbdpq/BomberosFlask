from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.asistencias import Asistencia_Cabecera, Asistencia_Detalle, Add_Cabecera
from scripts.db import Init_DB

bp = Blueprint('asistencias', __name__)

@bp.route('/', methods=['GET'])
def Asistencias():
    return render_template('asistencias/cargar_planilla.html')

@bp.route('/Test/1', methods=['POST'])
def Test():
    Add_Cabecera(1, '')
    flash('Test finalizado.')
    return redirect(url_for('asistencias.Asistencias'))

@bp.route('/Test/2', methods=['POST'])
def Limpiar():
    Init_DB(True)
    flash('Test finalizado.')
    return redirect(url_for('asistencias.Asistencias'))