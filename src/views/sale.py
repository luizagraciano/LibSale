from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/new')
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

        sale = db.execute(
            'SELECT * FROM sale WHERE id = (SELECT MAX(id) FROM sale)'
        ).fetchone()

        id = sale['id']

        return redirect(url_for('sale.update_sale', id = id))
    else:
        return redirect(url_for('dashboard.welcome'))
    

@bp.route('/<int:id>/')
def update_sale(id):

    db = get_db()
    sale_itens = db.execute(
        'SELECT * from sale_item WHERE sale_id = (SELECT MAX(id) FROM sale) ORDER BY id DESC'
    ).fetchall()

    return render_template('pos/sale.html', sale_itens = sale_itens)