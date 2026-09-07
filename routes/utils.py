from functools import wraps
from flask import abort, current_app
from flask_login import current_user

def encargado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.encargado:
            current_app.logger.warning(
                "manager_access_denied user_id=%s",
                current_user.id if current_user.is_authenticated else None,
            )
            abort(403) # Prohibido si no es encargado
        return f(*args, **kwargs)
    return decorated_function
