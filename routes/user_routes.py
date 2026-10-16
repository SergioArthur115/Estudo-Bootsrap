from flask import Blueprint, render_template, request, flash, redirect, url_for, g

from utils.decorators import login_required
from utils.user_form import apply_user_update

bp = Blueprint('user', __name__)


@bp.route('/noticias')
def noticias():
    return render_template('noticias.html')


@bp.route('/cavaleiros')
def cavaleiros():
    return render_template('cavaleiros.html')


@bp.route('/mortos_de_amor')
def mortos_de_amor():
    return render_template('mortos_de_amor.html')


@bp.route('/inuyasha')
def inuyasha():
    return render_template('inuyasha.html')


@bp.route('/dicria')
def dicria():
    return render_template('dicria.html')


@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        ok, msg = apply_user_update(g.user, request.form, request.files)
        flash(msg)
        return redirect(url_for('user.perfil'))  # evita reenvio do form no F5

    return render_template('perfil.html', user=g.user)
