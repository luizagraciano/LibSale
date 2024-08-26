import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from src.data.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_name = request.form ['user-name']
        user_id = request.form ['user-id']
        user_birthday = request.form ['user-birthday']
        user_phone = request.form ['user-phone-number']
        user_email = request.form ['user-email']
        user_password = request.form ['user-password']
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute(
                    "INSERT INTO seller (id, name, birthday, phone_number, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, user_name, user_birthday, user_phone, user_email, generate_password_hash(user_password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Usuário já cadastrado."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request.form ['user-id']
        user_password = request.form ['user-password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM seller WHERE id = ?', (user_id,)
        ).fetchone()

        if user is None:
            error = 'Usuário ou senha incorreta.'
        elif not check_password_hash(user['password'], user_password):
            error = 'Usuário ou senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard.welcome'))

        flash(error)
        
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('home'))