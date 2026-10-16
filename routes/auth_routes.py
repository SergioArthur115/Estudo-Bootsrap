import sqlite3

from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, session, current_app)
from werkzeug.security import generate_password_hash, check_password_hash

from models.user_model import create_user, get_user_by_email
from utils.uploads import save_photo, delete_photo

bp = Blueprint('auth', __name__)


@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        sobrenome = request.form.get('sobrenome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        if not (nome and sobrenome and email and senha):
            flash('Preencha todos os campos obrigatórios.','danger')
            return redirect(url_for('auth.cadastro'))

        default = current_app.config['DEFAULT_PHOTO']
        try:
            filename = save_photo(request.files.get('foto'), default)
        except ValueError as e:
            flash(str(e),'danger')
            return redirect(url_for('auth.cadastro'))

        try:
            create_user(nome, sobrenome, email, generate_password_hash(senha), filename)
        except sqlite3.IntegrityError:  # UNIQUE do banco: sem race condition
            if filename != default:
                delete_photo(filename)
            flash('E-mail já cadastrado','danger')
            return redirect(url_for('auth.cadastro'))

        flash('Cadastro realizado','success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = get_user_by_email(email)

        if user and check_password_hash(user['senha'], request.form.get('senha', '')):
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('admin.admin' if user['is_admin'] else 'user.perfil'))

        flash('Login inválido','danger')

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.','info')
    return redirect(url_for('auth.login'))
