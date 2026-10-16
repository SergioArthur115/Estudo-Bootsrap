import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Em produção defina SECRET_KEY como variável de ambiente.
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-troque-em-producao')

DATABASE = os.path.join(BASE_DIR, 'database.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # limite de upload: 2 MB

# Foto padrão (o arquivo precisa existir em static/uploads/)
DEFAULT_PHOTO = 'default.jpg'

# Admin criado automaticamente na primeira execução (apenas se não houver admin)
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@gmail.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '123456')
