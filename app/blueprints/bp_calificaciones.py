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
    return render_template('calificaciones/semestral.html', calificaciones=Calificacion.Get_Semestral(), Bombero=Bombero)

@bp.route('/anual', methods=['GET'])
def Anual():
    return render_template('calificaciones/anual.html', calificaciones=Calificacion.Get_Anual(), Bombero=Bombero)