from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from scripts.personal import Bombero
from scripts.eventos import Evento
from scripts.unidades import Unidad
from scripts.asistencias import Asistencia_Cabecera, Asistencia_Detalle, Add_Cabecera
from scripts.db import Init_DB

bp = Blueprint('asistencias', __name__)

@bp.route('/cargar/', methods=['GET'])
def Index():
    return render_template('asistencias/cargar_planilla.html', eventos=Evento.Get_Eventos())

@bp.route('/cargar/<evento_nombre>', methods=['POST'])
def Nueva_Planilla(evento_nombre):
    evento = Evento.Get_Evento_By_Nombre(evento_nombre)
    id_cabecera = Add_Cabecera(evento.id)
    
    flash('Planilla de asistencias cargada correctamente.')
    return render_template('asistencias/cargar_planilla_detalle.html', cabecera=Asistencia_Cabecera.Get_Asistencia_By_ID(id_cabecera), evento=evento, bomberos=Bombero.Get_Bomberos(), unidades=Unidad.Get_Unidades())

@bp.route('/Test/1', methods=['POST'])
def Test():
    Add_Cabecera(1, '')
    flash('Test finalizado.')
    return redirect(url_for('asistencias.Index'))

@bp.route('/Test/2', methods=['POST'])
def Limpiar():
    Init_DB(True)
    flash('Test finalizado.')
    return redirect(url_for('asistencias.Index'))