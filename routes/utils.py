from functools import wraps
from flask import abort
from flask_login import current_user

def encargado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.encargado:
            abort(403) # Prohibido si no es encargado
        return f(*args, **kwargs)
    return decorated_function