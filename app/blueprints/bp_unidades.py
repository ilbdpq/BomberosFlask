from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.unidades import Unidad

bp = Blueprint('unidades', __name__)

@bp.route('/', methods=['GET'])
def Unidades():
    return render_template('datos/unidades.html', unidades=Unidad.Get_Unidades())

@bp.route('/subir', methods=['POST'])
def Subir():
    id = request.form['id']
    nombre = request.form['nombre']
    estado = request.form['estado']

    unidad = Unidad(
        id=id,
        nombre=nombre,
        estado=estado
    )

    if unidad.id == '' or Unidad.Get_Unidad_By_ID(unidad.id) is None:
        unidad.Add()

    else:
        unidad.Set()

    flash('Unidad agregada/actualizada exitosamente.')
    return redirect(url_for('unidades.Unidades'))