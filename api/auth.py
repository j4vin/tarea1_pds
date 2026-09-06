import re
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

def es_formato_valido(correo):
    patron = r"^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@(profesor|alumno)\.usm\.cl$"
    return re.match(patron, correo) is not None

def extraer_datos_correo(correo):
    patron = r"^([a-zA-Z0-9]+)\.([a-zA-Z0-9]+)@(profesor|alumno)\.usm\.cl$"
    match = re.match(patron, correo)
    
    if match:
        return {
            "nombre_formateado": f"{match.group(1).capitalize()} {match.group(2).capitalize()}",
            "es_profesor": 1 if match.group(3) == "profesor" else 0
        }
    return None

@auth_bp.route('/api/validar_correo', methods=['POST'])
def validar_correo():
    datos = request.get_json()
    correo = datos.get('correo', '')
    
    # Solo devolvemos True o False para no gastar recursos
    return jsonify({"valido": es_formato_valido(correo)})