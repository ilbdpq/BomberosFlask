from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from functools import wraps
from scripts.personal import Bombero

def Admin_Required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Inicie sesión para acceder a esta página.')
            return redirect(url_for('index.Index'))
        
        elif session['user']['permisos'] < 2:
            flash('No tiene permisos de administrador para acceder a esta página.')
            return redirect(url_for('index.Index'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def User_Required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Inicie sesión para acceder a esta página.')
            return redirect(url_for('index.Index'))
        
        elif session['user']['permisos'] < 1:
            flash('No tiene permisos de usuario para acceder a esta página.')
            return redirect(url_for('index.Index'))
        
        return f(*args, **kwargs)
    
    return decorated_function

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
def Index():
    try:
        user = session['user']
        
        if user['permisos'] == 2:
            return render_template('index/index_admin.html', bombero=user)
        
        elif user['permisos'] == 1:
            return render_template('index/index_user.html', bombero=user)
        
    except KeyError:
        return render_template('index/index_login.html')

@bp.route('/login', methods=['POST'])
def Login():
    username = request.form['username']
    password = request.form['password']
    
    bombero = Bombero.Get_Bombero_By_Username(username)
    
    if not bombero:
        bombero = Bombero.Get_Bombero_By_Legajo(username)
    
    if not bombero:
        bombero = Bombero.Get_Bombero_By_DNI(username)
    
    if bombero:
        if bombero.password == password:
            session['user'] = {
                'legajo': bombero.legajo,
                'username': bombero.username,
                'apellido_nombre': bombero.apellido_nombre,
                'permisos': bombero.permisos,
            }
            session['tema'] = 'color' # Tema por defecto
            session.permanent = True # Mantener la sesión activa
            
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

@bp.route('/tema', methods=['POST'])
def Tema():
    tema_actual = session.get('tema', 'color')
    
    if tema_actual == 'color':
        session['tema'] = 'bw'
        
    else:
        session['tema'] = 'color'
    
    return redirect(request.referrer or url_for('index.Index'))