import sqlite3

from models.user_model import update_user
from utils.uploads import save_photo, delete_photo


def apply_user_update(user, form, files):
    """Valida e grava nome, sobrenome, e-mail e foto (usado pelo perfil e pelo admin).

    Retorna (sucesso: bool, mensagem: str).
    """
    nome = form.get('nome', '').strip()
    sobrenome = form.get('sobrenome', '').strip()
    email = form.get('email', '').strip().lower()

    if not (nome and sobrenome and email):
        return False, 'Preencha nome, sobrenome e e-mail.'

    try:
        filename = save_photo(files.get('foto'), user['foto'])
    except ValueError as e:
        return False, str(e)

    try:
        update_user(user['id'], nome, sobrenome, email, filename)
    except sqlite3.IntegrityError:
        if filename != user['foto']:
            delete_photo(filename)  # descarta o upload que não foi usado
        return False, 'Este e-mail já está em uso.'

    if filename != user['foto']:
        delete_photo(user['foto'])  # remove a foto antiga substituída
    return True, 'Dados atualizados com sucesso!'
