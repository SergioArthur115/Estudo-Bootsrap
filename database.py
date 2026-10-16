import sqlite3
from contextlib import contextmanager

from werkzeug.security import generate_password_hash

from config import DATABASE, ADMIN_EMAIL, ADMIN_PASSWORD, DEFAULT_PHOTO


@contextmanager
def get_db():
    """Abre a conexão, faz commit/rollback e SEMPRE fecha."""
    conn = sqlite3.connect(DATABASE, timeout=10)  # espera o lock em vez de falhar na hora
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    # lower() do Python entende acentos; o do SQLite só ASCII
    conn.create_function(
        'py_lower', 1,
        lambda s: s.lower() if isinstance(s, str) else s,
        deterministic=True,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute('PRAGMA journal_mode = WAL')  # melhor concorrência leitura/escrita

        # Estrutura mantida exatamente como no banco atual
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                foto TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        ''')

        admin = conn.execute('SELECT 1 FROM users WHERE is_admin = 1').fetchone()
        if not admin:
            conn.execute(
                'INSERT INTO users (nome, sobrenome, email, senha, foto, is_admin) '
                'VALUES (?, ?, ?, ?, ?, 1)',
                ('Admin', 'Sistema', ADMIN_EMAIL.lower(),
                 generate_password_hash(ADMIN_PASSWORD), DEFAULT_PHOTO)
            )


if __name__ == '__main__':
    init_db()
    print('Banco de dados criado/atualizado com sucesso!')
