import os
import uuid

from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def save_photo(file, current=None):
    """Salva a foto enviada e devolve o nome gerado.

    Sem upload, devolve `current` (mantém a foto atual).
    Levanta ValueError se a extensão não for permitida.
    """
    if not file or not file.filename:
        return current

    name = file.filename
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError('Formato de imagem não permitido (use png, jpg, jpeg, gif ou webp).')

    filename = f'{uuid.uuid4().hex}.{ext}'
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return filename


def delete_photo(filename):
    """Remove a foto do disco, preservando as fotos padrão (default.*)."""
    if not filename:
        return
    filename = os.path.basename(filename)
    if os.path.splitext(filename)[0] == 'default':
        return
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(path):
        os.remove(path)
