from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from database.models import db, Usuario 
from api.auth import es_formato_valido, extraer_datos_correo

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        if not es_formato_valido(correo):
            return "Error: El correo no tiene el formato correcto.", 400

        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            return "Este correo ya está registrado.", 400
        
        datos_extraidos = extraer_datos_correo(correo)
        pass_encriptada = generate_password_hash(contraseña)

        nuevo_usuario = Usuario(
            nombre=datos_extraidos["nombre_formateado"],
            correo=correo,
            contraseña=pass_encriptada,
            profesor=bool(datos_extraidos["es_profesor"])
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return "Cuenta creada exitosamente."

    return render_template('registro.html')