from database import get_db

# Nunca devolve o hash da senha, exceto em get_user_by_email (necessário no login)
SAFE_COLUMNS = 'id, nome, sobrenome, email, foto, is_admin'

# Whitelist: ORDER BY não aceita parâmetro "?", então só colunas conhecidas entram na query
ORDER_COLUMNS = {'nome', 'email'}

_WHERE = "WHERE py_lower(nome) LIKE ? ESCAPE '\\' OR py_lower(email) LIKE ? ESCAPE '\\'"


def _like(term):
    escaped = term.lower().replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    return f'%{escaped}%'


def create_user(nome, sobrenome, email, senha_hash, foto):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO users (nome, sobrenome, email, senha, foto) VALUES (?,?,?,?,?)',
            (nome, sobrenome, email, senha_hash, foto)
        )


def get_user_by_email(email):
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM users WHERE lower(email) = lower(?)', (email,)
        ).fetchone()


def get_user_by_id(user_id):
    with get_db() as conn:
        return conn.execute(
            f'SELECT {SAFE_COLUMNS} FROM users WHERE id = ?', (user_id,)
        ).fetchone()


def search_users(search, order, page, per_page):
    """Busca, ordena e pagina direto no SQL. Retorna (linhas, total)."""
    order = order if order in ORDER_COLUMNS else 'nome'
    like = _like(search)
    with get_db() as conn:
        total = conn.execute(
            f'SELECT COUNT(*) FROM users {_WHERE}', (like, like)
        ).fetchone()[0]
        rows = conn.execute(
            f'SELECT {SAFE_COLUMNS} FROM users {_WHERE} '
            f'ORDER BY py_lower({order}) LIMIT ? OFFSET ?',
            (like, like, per_page, (page - 1) * per_page)
        ).fetchall()
    return rows, total


def update_user(user_id, nome, sobrenome, email, foto):
    with get_db() as conn:
        conn.execute(
            'UPDATE users SET nome=?, sobrenome=?, email=?, foto=? WHERE id=?',
            (nome, sobrenome, email, foto, user_id)
        )


def delete_user(user_id):
    with get_db() as conn:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
