from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db
from src.views.sale import get_last_sale

bp = Blueprint('cash_register', __name__, url_prefix='/cash_register')

@bp.route('/open', methods=('GET', 'POST'))
def open():
    db = get_db()

    if request.method == "POST":
        seller_id = session['user_id']
        status = "Aberto"
        cash_fund = request.form['cash-fund']
        error = None

        if error is None:
            try:
                db.execute(
                    "INSERT INTO cash_register (seller_id, status, cash_fund) VALUES (?, ?, ?)",
                    (seller_id, status, cash_fund),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Caixa já aberto"
            else:
                return redirect(url_for('dashboard.welcome'))

    try:
        cash = db.execute(
            'SELECT * FROM cash_register WHERE id = (SELECT MAX(id) FROM cash_register)'
        ).fetchone()

        if cash['status'] == 'Fechado':
            return render_template('pos/open.html')
        else:
            return redirect(url_for('dashboard.welcome'))
    except TypeError:
        return render_template('pos/open.html')
    

@bp.route('/close', methods=('GET', 'POST'))
def close():
    db = get_db()
    
    if request.method == "POST":
        status = "Fechado"
        revenue_declared = request.form['revenue']
        expenses_declared = request.form['expenses']
        error = None

        if error is None:
            try:
                db.execute(
                    "UPDATE cash_register SET status = ?, revenue_declared = ?, expenses_declared = ? WHERE id = (SELECT MAX(id) FROM cash_register)",
                    (status, revenue_declared, expenses_declared),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Caixa já fechado"
            else:
                return redirect(url_for('dashboard.welcome'))

    try:
        cash = db.execute(
            'SELECT * FROM cash_register WHERE id = (SELECT MAX(id) FROM cash_register)'
        ).fetchone()

        if cash['status'] == 'Aberto':
            return render_template('pos/close.html', cash=cash)
        else:
            return redirect(url_for('dashboard.welcome'))
    except TypeError:
        return render_template('pos/close.html', cash=cash)

@bp.route('/update')
def update():
    sale = get_last_sale()
    db = get_db()
    db.execute(
        'UPDATE cash_register SET revenue = (revenue + ?), sales_number = sales_number + 1, products_sold = (products_sold + ?) WHERE id = (SELECT MAX(id) FROM cash_register)',
        (sale['sale_total_price'], sale['itens_quantity'])
    )
    db.commit()
    
    return redirect(url_for('dashboard.welcome'))