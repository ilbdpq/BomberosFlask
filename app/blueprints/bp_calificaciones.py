from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.calificaciones import Calificacion
from scripts.personal import Bombero
from scripts.eventos import Evento
from blueprints.bp_index import Login_Required

bp = Blueprint('calificaciones', __name__)

@bp.route('/mensual', methods=['GET'])
def Mensual():
    return render_template('calificaciones/mensual.html', calificaciones=Calificacion.Get_Mensual(), Calificacion=Calificacion, Bombero=Bombero, Evento=Evento)

@bp.route('/semestral', methods=['GET'])
def Semestral():
    return render_template('calificaciones/semestral.html', calificaciones=Calificacion.Get_Semestral(), Calificacion=Calificacion, Bombero=Bombero, Evento=Evento)

@bp.route('/anual', methods=['GET'])
def Anual():
    return render_template('calificaciones/anual.html', calificaciones=Calificacion.Get_Anual(), Calificacion=Calificacion, Bombero=Bombero, Evento=Evento)

@bp.route('/historico', methods=['GET'])
def Historico():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    return render_template(
        'calificaciones/historico.html',
        calificaciones=Calificacion.Get_Historico(fecha_inicio, fecha_fin),
        Calificacion=Calificacion, Bombero=Bombero, Evento=Evento,
        fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
    )