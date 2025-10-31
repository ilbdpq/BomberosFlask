from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from scripts.personal import Bombero

bp = Blueprint('personal', __name__)

@bp.route('/personal/', methods=['GET'])
def Personal():
    return render_template('datos/personal.html', personal=Bombero.Get_Personal_List())