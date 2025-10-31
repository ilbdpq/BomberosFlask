from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.personal import Bombero

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
def Index():
    try:
        user = session['user']
        bombero = Bombero.Get_Bombero_By_Username(user)
        
        if bombero.permisos == 1:
            return render_template('index/index_admin.html', bombero=bombero)
        
        else:
            return render_template('index/index_user.html', bombero=bombero)
        
    except KeyError:
        return render_template('index/index_login.html')

@bp.route('/login', methods=['POST'])
def Login():
    username = request.form['username']
    password = request.form['password']
    
    # Aquí iría la lógica de autenticación
    bombero = Bombero.Get_Bombero_By_Username(username)
    
    if not bombero:
        bombero = Bombero.Get_Bombero_By_Legajo(username)
    
    if not bombero:
        bombero = Bombero.Get_Bombero_By_DNI(username)
    
    if bombero:
        if bombero.password == password:
            session['user'] = bombero.username
            session.permanent = True  # Mantener la sesión activa
            
            return redirect(url_for('index.Index'))
        
        else:
            flash('Contraseña inválida')
            return redirect(url_for('index.Index'))
        
    else:
        flash('Usuario, legajo o DNI no encontrado')
        return redirect(url_for('index.Index'))
    
@bp.route('/logout', methods=['POST'])
def Logout():
    session.clear()
    return redirect(url_for('index.Index'))