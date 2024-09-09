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


def get_product(id):
    db = get_db()
    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (id,)
    ).fetchone()

    return product

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def update_sale(id):

    if request.method == 'POST':
        product_id = request.form['product-id']

        product = get_product(product_id)

        db = get_db()
        db.execute(
            'INSERT INTO sale_item (product_id, product_price, quantity, subtotal, sale_id) VALUES (?, ?, ?, ?, ?)',
            (product['id'], product['price'], '1', product['price'], id)
        )
        db.commit()

    db = get_db()
    sale_itens = db.execute(
        'SELECT p.name, si.product_id, p.price, si.quantity, si.subtotal FROM sale_item si JOIN product p ON p.id = si.product_id WHERE si.sale_id = ?', (id,)
    ).fetchall()

    return render_template('pos/sale.html', sale_itens = sale_itens)