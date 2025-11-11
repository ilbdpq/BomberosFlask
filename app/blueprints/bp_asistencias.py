from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import datetime

from scripts.personal import Bombero
from scripts.eventos import Evento
from scripts.unidades import Unidad
from scripts.asistencias import Asistencia_Cabecera, Asistencia_Detalle, Add_Cabecera, Verificar_Conducta_Mes
from scripts.db import Init_DB

from blueprints.bp_index import Login_Required

bp = Blueprint('asistencias', __name__)

@bp.route('/cargar/', methods=['GET'])
@Login_Required
def Index():
    return render_template('asistencias/cargar_planilla.html', eventos=Evento.Get_Eventos())

@bp.route('/cargar/<evento_nombre>', methods=['POST'])
@Login_Required
def Nueva_Planilla(evento_nombre):
    if evento_nombre != 'Conducta':
        evento = Evento.Get_Evento_By_Nombre(evento_nombre)
        id_cabecera = Add_Cabecera(evento.id)
        
        flash('Planilla de asistencias cargada correctamente.')
        return render_template('asistencias/cargar_planilla_detalle.html', cabecera=Asistencia_Cabecera.Get_By_ID(id_cabecera), evento=evento, bomberos=Bombero.Get_Bomberos(), unidades=Unidad.Get_Unidades())
    
    elif Verificar_Conducta_Mes():
        flash('Ya se ha cargado la planilla de conducta para este mes.')
        return redirect(url_for('asistencias.Index'))
    
    else:
        evento = Evento.Get_Evento_By_Nombre(evento_nombre)
        id_cabecera = Add_Cabecera(evento.id)
        
        flash('Planilla de conducta cargada correctamente.')
        return render_template('asistencias/cargar_conducta.html', cabecera=Asistencia_Cabecera.Get_By_ID(id_cabecera), evento=evento, bomberos=Bombero.Get_Bomberos())

@bp.route('/cargar/detalles', methods=['POST'])
@Login_Required
def Cargar_Detalles():
    id_cabecera = int(request.form['id_cabecera'])
    cabecera = Asistencia_Cabecera.Get_By_ID(id_cabecera)

    descripcion = request.form.get('descripcion')
    cabecera.descripcion = descripcion
    
    for bombero in Bombero.Get_Bomberos():
        estado = int(request.form[f'{bombero.legajo}_estado'])
        id_unidad = request.form.get(f'{bombero.legajo}_unidad')
        try:
            id_unidad = int(id_unidad)
        except (TypeError, ValueError):
            id_unidad = None
        
        detalle = Asistencia_Detalle(None, cabecera.id, bombero.legajo, id_unidad, estado)
        detalle.Add()
        cabecera.Add_Detalle(detalle)
        cabecera.Set()
    
    flash('Detalles de asistencias cargados correctamente.')
    return redirect(url_for('asistencias.Index'))

@bp.route('/verificar/', methods=['GET'])
@Login_Required
def Verificar_Planillas():
    return render_template('asistencias/verificar_planillas.html', planillas=Asistencia_Cabecera.Get_Pendientes(), Evento=Evento, Bombero=Bombero, Unidad=Unidad)

@bp.route('/verificar/si/<int:id>', methods=['POST'])
@Login_Required
def Aceptar_Planilla(id):
    cabecera = Asistencia_Cabecera.Get_By_ID(id)
    cabecera.fecha_aceptada = datetime.datetime.now().strftime('%Y-%m-%d')
    cabecera.legajo_responsable = session['user']['legajo']
    cabecera.Set()
    
    flash('Planilla aceptada correctamente.')
    return redirect(url_for('asistencias.Verificar_Planillas'))

@bp.route('/verificar/no/<int:id>', methods=['POST'])
@Login_Required
def Rechazar_Planilla(id):
    cabecera = Asistencia_Cabecera.Get_By_ID(id)
    cabecera.Del()
    
    flash('Planilla rechazada y eliminada correctamente.')
    return redirect(url_for('asistencias.Verificar_Planillas'))

@bp.route('/ver/', methods=['GET'])
@Login_Required
def Ver_Planillas():
    return render_template('asistencias/ver_planillas.html', planillas=Asistencia_Cabecera.Get_Aceptadas(), Evento=Evento, Bombero=Bombero, Unidad=Unidad)

@bp.route('/Test/2', methods=['POST'])
@Login_Required
def Limpiar():
    Init_DB(True)
    flash('Test finalizado.')
    return redirect(url_for('asistencias.Index'))