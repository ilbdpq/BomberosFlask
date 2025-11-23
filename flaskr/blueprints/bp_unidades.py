from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from ..scripts.unidades import Unidad
from .bp_index import Admin_Required

bp = Blueprint('unidades', __name__)

@bp.route('/', methods=['GET'])
@Admin_Required
def Unidades():
    return render_template('datos/unidades.html', unidades=Unidad.Get_Unidades())

@bp.route('/subir', methods=['POST'])
@Admin_Required
def Subir():
    id = request.form['id']
    nombre = request.form['nombre']
    patente = request.form['patente']
    estado = request.form['estado']

    unidad = Unidad(
        id=id,
        nombre=nombre,
        patente=patente,
        estado=estado if estado else 1
    )

    if unidad.id == '' or Unidad.Get_Unidad_By_ID(unidad.id) is None:
        unidad.Add()

    else:
        unidad.Set()

    flash('Unidad agregada/actualizada exitosamente.')
    return redirect(url_for('unidades.Unidades'))