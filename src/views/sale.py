from datetime import datetime
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
            'INSERT INTO sale (seller_id, cash_register_id) VALUES(?, ?)', (seller, current_cash['id'])
        )
        db.commit()

        last_sale = get_last_sale()
        id = last_sale['id']

        return redirect(url_for('sale.checkout', id = id))
    else:
        return redirect(url_for('dashboard.welcome'))


@bp.route('/<int:id>/', methods=('GET', 'POST'))
def checkout(id):

    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y")
    sale = get_last_sale()

    if request.method == 'POST' and 'submit-add' in request.form:
        product_id = request.form['product-id']

        product = get_product(product_id)

        db = get_db()
        db.execute(
            'INSERT INTO sale_item (product_id, product_price, quantity, subtotal, sale_id) VALUES (?, ?, ?, ?, ?)',
            (product['id'], product['price'], '1', product['price'] , id)
        )
        db.commit()
        
        return redirect(url_for('sale.update_sale', id = id))
    

    if request.method == 'POST' and 'submit-checkout' in request.form:
        payment_method = request.form['payment-method']
        costumer = request.form['costumer']

        db = get_db()
        db.execute(
            'UPDATE sale SET payment_method = ?, status = ? WHERE id = ?', (payment_method, 'Concluída', id)
        )
        db.commit()

        if costumer != '':
            db.execute(
            'UPDATE sale SET costumer_id = ? WHERE id = ?', (costumer, id)
        )
        db.commit()

        return redirect(url_for('cash_register.update'))

    db = get_db()
    sale_itens = db.execute(
        'SELECT p.name, p.author, si.id, si.product_id, p.price, si.quantity, si.subtotal FROM sale_item si JOIN product p ON p.id = si.product_id WHERE si.sale_id = ? ORDER BY si.id DESC', (id,)
    ).fetchall()


    return render_template('pos/sale.html', sale_itens = sale_itens, sale = sale, date_time = date_time)


@bp.route('/<int:id>/update')
def update_sale(id):
    db = get_db()

    try:
        sale = db.execute(
            'SELECT SUM(quantity) AS quantity, SUM(subtotal) AS total FROM sale_item JOIN sale ON sale_item.sale_id = sale.id WHERE sale_id = (SELECT max(id) from sale)'
        ).fetchone()

        db.execute(
            'UPDATE sale SET itens_quantity = ?, sale_total_price = ? WHERE id = ?', (sale['quantity'], sale['total'], id)
        )
        db.commit()

    except db.IntegrityError:
        db.execute(
            'UPDATE sale SET itens_quantity = 0, sale_total_price = 0 WHERE id = ?', (id,)
        )
        db.commit()

    return redirect(url_for('sale.checkout', id = id))

@bp.route('/<int:id>/cancel')
def cancel_sale(id):
    db = get_db()

    db.execute(
        'DELETE FROM sale WHERE id = ?', (id,)
    )
    db.commit()

    return redirect(url_for('dashboard.welcome'))


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

    return redirect(url_for('sale.update_sale', id = id))


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

    return redirect(url_for('sale.update_sale', id = id))


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

    return redirect(url_for('sale.update_sale', id = id))


