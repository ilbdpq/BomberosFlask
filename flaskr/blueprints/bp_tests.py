from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import datetime
import random

from scripts.personal import Bombero
from scripts.eventos import Evento
from scripts.unidades import Unidad
from scripts.asistencias import Asistencia_Cabecera, Asistencia_Detalle, Add_Cabecera
from scripts.db import Get_DB

from blueprints.bp_index import Admin_Required

bp = Blueprint('tests', __name__)

@bp.route('/asistencias/generar', methods=['POST'])
@Admin_Required
def Generar_Planillas():
    # Generar planillas con fechas aleatorias
    for _ in range(100):
        id_evento = random.randint(1, 4)
        fecha_creada = datetime.date(random.randint(2024, 2025), random.randint(1, 6), random.randint(1, 28))
        id_cabecera = Add_Cabecera(id_evento, fecha_creada.strftime('%Y-%m-%d'))
        
        for bombero in Bombero.Get_Bomberos():
            estado = random.randint(0, 2)
            id_unidad = random.choice([unidad.id for unidad in Unidad.Get_Unidades()] + [None])
            detalle = Asistencia_Detalle(None, id_cabecera, bombero.legajo, id_unidad, estado)
            detalle.Add()
            
        cabecera = Asistencia_Cabecera.Get_By_ID(id_cabecera)
        cabecera.fecha_aceptada = datetime.datetime.now().strftime('%Y-%m-%d')
        cabecera.legajo_responsable = session['user']['legajo']
        cabecera.Set()
            
    flash('Planillas de asistencias generadas correctamente.')
    return redirect(url_for('index.Index'))

@bp.route('/asistencias/generar_mes', methods=['POST'])
@Admin_Required
def Generar_Planillas_Mes():
    # Generar planillas para el mes actual
    hoy = datetime.date.today()
    primer_dia = hoy.replace(day=1)
    ultimo_dia = (primer_dia + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    
    for dia in range(primer_dia.day, ultimo_dia.day + 1):
        fecha_creada = primer_dia.replace(day=dia)
        id_evento = random.randint(1, 4)
        id_cabecera = Add_Cabecera(id_evento, fecha_creada.strftime('%Y-%m-%d'))
        
        for bombero in Bombero.Get_Bomberos():
            estado = random.randint(0, 2)
            id_unidad = random.choice([unidad.id for unidad in Unidad.Get_Unidades()] + [None])
            detalle = Asistencia_Detalle(None, id_cabecera, bombero.legajo, id_unidad, estado)
            detalle.Add()
        
        cabecera = Asistencia_Cabecera.Get_By_ID(id_cabecera)
        cabecera.fecha_aceptada = datetime.datetime.now().strftime('%Y-%m-%d')
        cabecera.legajo_responsable = session['user']['legajo']
        cabecera.Set()
            
    flash('Planillas de asistencias para el mes generadas correctamente.')
    return redirect(url_for('index.Index'))

@bp.route('/asistencias/borrar', methods=['POST'])
@Admin_Required
def Borrar_Planillas():
    DB = Get_DB()
    CUR = DB.cursor()
    CUR.execute('DELETE FROM asistencias_det')
    CUR.execute('DELETE FROM asistencias_cab')
    DB.commit()
    
    flash('Todas las planillas de asistencias han sido borradas.')
    return redirect(url_for('index.Index'))