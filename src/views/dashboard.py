import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
from src.data.db import get_db
from src.views import auth

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=('GET', 'POST'))
def welcome():
    if 'user_id' in session:
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y")
        return render_template('pos/dashboard.html', date_time=date_time)
    return redirect(url_for('auth.login'))