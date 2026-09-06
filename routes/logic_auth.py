from database.models import Usuario

def verificar_credenciales(correo, password):
    # Buscamos al usuario por correo
    usuario = Usuario.query.filter_by(correo=correo).first()
    
    # Verificamos si existe y si la contraseña coincide (texto plano para prototipo)
    if usuario and usuario.contraseña == password:
        return usuario
    return None