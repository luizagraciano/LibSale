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

        db = get_db()

        current_cash = db.execute(
            'SELECT * FROM cash_register WHERE id = (SELECT MAX(id) FROM cash_register)'
        ).fetchone()

        daily_cash = db.execute(
            'SELECT SUM(revenue), SUM(sales_number), SUM(products_sold) FROM cash_register WHERE DATE(cash_date) = CURRENT_DATE'
        ).fetchone()
        
        return render_template('pos/dashboard.html', date_time=date_time, current_cash=current_cash, daily_cash=daily_cash)

    return redirect(url_for('auth.login'))