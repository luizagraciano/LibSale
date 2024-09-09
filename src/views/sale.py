from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/')
def new_sale():

    db = get_db()

    current_cash = db.execute(
        'SELECT * FROM cash_register WHERE id = (SELECT MAX(id) FROM cash_register)'
    ).fetchone()

    status = current_cash['status']
    seller = session['user_id']

    if status == 'Aberto':
        db.execute(
            'INSERT INTO sale (seller_id) VALUES(?)', (seller,)
        )
        db.commit()

        return render_template('pos/sale.html')
    else:
        return redirect(url_for('dashboard.welcome'))
    

