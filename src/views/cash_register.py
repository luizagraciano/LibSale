from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('cash_register', __name__, url_prefix='/cash_register')

@bp.route('/open', methods=('GET', 'POST'))
def open():
    if request.method == "POST":
        seller_id = session['user_name']
        status = "Aberto"
        cash_fund = request.form['cash-fund']
        revenue = 0
        expenses = 0
        sales_number = 0
        products_sold = 0
        sales_income = 0
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute(
                    "INSERT INTO cash_register (seller_id, status, cash_fund, revenue, expenses, sales_number, products_sold, sales_income) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (seller_id, status, cash_fund, revenue, expenses, sales_number, products_sold, sales_income),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Caixa já aberto"
            else:
                return redirect(url_for('dashboard.welcome'))

    return render_template('pos/open.html')

@bp.route('/close', methods=('GET', 'POST'))
def close():
    db = get_db()
    cash = db.execute(
            'SELECT * FROM cash_register WHERE id = (SELECT MAX(id) FROM cash_register)'
        ).fetchone()
    
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
            
    return render_template('pos/close.html', cash=cash)