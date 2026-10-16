import math

from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, abort)

from models.user_model import search_users, get_user_by_id, delete_user
from utils.decorators import admin_required
from utils.uploads import delete_photo
from utils.user_form import apply_user_update

bp = Blueprint('admin', __name__)

PER_PAGE = 10


@bp.route('/admin')
@admin_required
def admin():
    search = request.args.get('search', '').strip()
    order = request.args.get('order', 'nome')
    page = max(request.args.get('page', 1, type=int), 1)

    users, total = search_users(search, order, page, PER_PAGE)

    return render_template(
        'admin.html',
        users=users,
        page=page,
        total_pages=math.ceil(total / PER_PAGE),
        search=search,
        order=order,
    )


@bp.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404)

    if request.method == 'POST':
        ok, msg = apply_user_update(user, request.form, request.files)
        flash(msg, 'success' if ok else 'danger')
        if ok:
            return redirect(url_for('admin.admin'))
        return redirect(url_for('admin.edit', user_id=user_id))

    return render_template('edit_user.html', user=user)


@bp.route('/admin/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404)

    if session['user_id'] == user_id:
        flash('Você não pode excluir a si mesmo.','warning')
    else:
        delete_user(user_id)
        delete_photo(user['foto'])
        flash('Usuário excluído.','success')

    return redirect(url_for('admin.admin'))
