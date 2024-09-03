from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('cash_register', __name__, url_prefix='/cash_register')

@bp.route('/open', methods=('GET', 'POST'))
def open():
    return render_template('pos/open.html')

@bp.route('/close', methods=('GET', 'POST'))
def close():
    return render_template('pos/close.html')