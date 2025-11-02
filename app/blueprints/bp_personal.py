from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.personal import Bombero

bp = Blueprint('personal', __name__)

@bp.route('/', methods=['GET'])
def Personal():
    return render_template('datos/personal.html', personal=Bombero.Get_Bomberos())

@bp.route('/subir', methods=['POST'])
def Subir():
    legajo = request.form['legajo']
    dni = request.form['dni']
    username = request.form['username']
    password = request.form['password']
    apellido_nombre = request.form['apellido_nombre']
    telefono = request.form['telefono']
    fecha_nacimiento = request.form['fecha_nacimiento']
    provincia = request.form['provincia']
    lugar = request.form['lugar']
    permisos = request.form['permisos']

    bombero = Bombero(
        legajo=legajo,
        dni=dni,
        username=username,
        password=password,
        apellido_nombre=apellido_nombre,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento,
        provincia=provincia,
        lugar=lugar,
        permisos=permisos
    )

    if Bombero.Get_Bombero_By_Legajo(legajo) is None:
        bombero.Add()

    else:
        bombero.Set()

    flash('Bombero agregado/actualizado exitosamente.')
    return redirect(url_for('personal.Personal'))