from functools import wraps

from flask import session, redirect, url_for, abort, g

from models.user_model import get_user_by_id


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_by_id(session['user_id']) if 'user_id' in session else None
        if user is None:  # não logado, ou usuário excluído com sessão ainda ativa
            session.clear()
            return redirect(url_for('auth.login'))
        g.user = user     # as rotas reaproveitam, sem nova consulta
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.user['is_admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated
