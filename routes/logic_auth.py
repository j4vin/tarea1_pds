from database.models import Usuario
from werkzeug.security import check_password_hash

def verificar_credenciales(correo, password):
    # Buscamos al usuario por correo
    usuario = Usuario.query.filter_by(correo=correo).first()
    
    # La contraseña se guarda como hash durante el registro, por lo que debe
    # comprobarse con la función segura de Werkzeug.
    if usuario and check_password_hash(usuario.contraseña, password):
        return usuario
    return None
