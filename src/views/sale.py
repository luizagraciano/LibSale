from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.data.db import get_db

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/', methods=('GET', 'POST'))
def new_sale():
    return render_template('pos/sale.html')