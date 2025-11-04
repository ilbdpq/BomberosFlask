from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.eventos import Evento

bp = Blueprint('eventos', __name__)

@bp.route('/', methods=['GET'])
def Eventos():
    return render_template('datos/eventos.html', eventos=Evento.Get_Eventos())

@bp.route('/subir', methods=['POST'])
def Subir():
    id = request.form['id']
    nombre = request.form['nombre']
    puntos = request.form['puntos']

    evento = Evento(
        id=id,
        nombre=nombre,
        puntos=puntos
    )

    if evento.id == '' or Evento.Get_Evento_By_ID(evento.id) is None:
        evento.Add()

    else:
        evento.Set()

    flash('Evento agregado/actualizado exitosamente.')
    return redirect(url_for('eventos.Eventos'))