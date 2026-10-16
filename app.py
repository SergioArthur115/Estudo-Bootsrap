import os

from flask import Flask, render_template, session, g
from flask_wtf.csrf import CSRFProtect

from database import init_db
from models.user_model import get_user_by_id
from routes.auth_routes import bp as auth_bp
from routes.user_routes import bp as user_bp
from routes.admin_routes import bp as admin_bp
from data.noticias import NOTICIAS

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    csrf.init_app(app)
    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_user():
        """Disponibiliza `current_user` em todos os templates (usado no header)."""
        user = g.get('user')
        if user is None and 'user_id' in session:
            user = get_user_by_id(session['user_id'])
        return {'current_user': user}

    @app.route('/')
    def index():
        return render_template('index.html', noticias=NOTICIAS)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1')
