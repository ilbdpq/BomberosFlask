from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('index', __name__)

@bp.route('/')
def Index():
    return render_template('index/index.html')