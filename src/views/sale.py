from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('sale', __name__, url_prefix='/sale')

def get_last_sale():
    db = get_db()
    sale = db.execute(
            'SELECT * FROM sale WHERE id = (SELECT MAX(id) FROM sale)'
        ).fetchone()

    return sale

    
def get_item(id):
    db = get_db()
    item = db.execute(
        'SELECT * FROM sale_item WHERE id = ?', (id,)
    ).fetchone()

    return item

def get_product(id):
    db = get_db()
    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (id,)
    ).fetchone()

    return product


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

        last_sale = get_last_sale()
        id = last_sale['id']

        return redirect(url_for('sale.checkout', id = id))
    else:
        return redirect(url_for('dashboard.welcome'))


@bp.route('/<int:id>/', methods=('GET', 'POST'))
def checkout(id):

    if request.method == 'POST':
        product_id = request.form['product-id']

        product = get_product(product_id)

        db = get_db()
        db.execute(
            'INSERT INTO sale_item (product_id, product_price, quantity, subtotal, sale_id) VALUES (?, ?, ?, ?, ?)',
            (product['id'], product['price'], '1', product['price'] , id)
        )
        db.commit()
        
        return redirect(url_for('sale.checkout', id = id))

    db = get_db()
    sale_itens = db.execute(
        'SELECT p.name, p.author, si.id, si.product_id, p.price, si.quantity, si.subtotal FROM sale_item si JOIN product p ON p.id = si.product_id WHERE si.sale_id = ? ORDER BY si.id DESC', (id,)
    ).fetchall()

    sale = get_last_sale()

    return render_template('pos/sale.html', sale_itens = sale_itens, sale = sale)

'''@bp.route('/<int:id>/update')
def update_sale(id):
    db = get_db()
    db.execute(
        ''
    )'''



@bp.route('/<int:id>/plus')
def plus_item(id):
    get_item(id)

    db = get_db()
    db.execute(
        'UPDATE sale_item SET quantity = quantity +1 WHERE id = ?', (id,)
        )
    db.commit()

    db.execute(
        'UPDATE sale_item SET subtotal = product_price * quantity WHERE id = ?', (id,)
        )
    db.commit()

    last_sale = get_last_sale()
    id = last_sale['id']

    return redirect(url_for('sale.checkout', id = id))


@bp.route('/<int:id>/minus')
def minus_item(id):
    get_item(id)

    db = get_db()
    db.execute(
        'UPDATE sale_item SET quantity = quantity -1 WHERE id = ?', (id,)
        )
    db.commit()

    db.execute(
        'UPDATE sale_item SET subtotal = product_price * quantity WHERE id = ?', (id,)
        )
    db.commit()

    last_sale = get_last_sale()
    id = last_sale['id']

    return redirect(url_for('sale.checkout', id = id))


@bp.route('/<int:id>/delete')
def delete_item(id):
    get_item(id)

    db = get_db()
    db.execute(
        'DELETE FROM sale_item WHERE id = ?', (id,)
        )
    db.commit()

    last_sale = get_last_sale()
    id = last_sale['id']

    return redirect(url_for('sale.checkout', id = id))


