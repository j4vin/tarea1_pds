from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required



from .utils import encargado_required
from database.models import Solicitud, Equipo
from .logic_encargado_solicitudes import gestionar_solicitud, obtener_solicitudes_progreso_ordenadas
from .logic_enc_equipos import registrar_nuevo_equipo, modificar_disponibilidad


encargado_bp = Blueprint('encargado', __name__, url_prefix='/Encargado')

@encargado_bp.route('/solicitudes/pendientes')
@login_required
@encargado_required
def pendientes():
    sols = Solicitud.query.filter_by(estado='pendiente').all()
    return render_template('enc_sol_pendientes.html', solicitudes=sols)

@encargado_bp.route('/solicitudes/en_progreso')
@login_required
@encargado_required
def en_progreso():
    
    sols = obtener_solicitudes_progreso_ordenadas()
    return render_template('enc_sol_progreso.html', solicitudes=sols)

@encargado_bp.route('/solicitudes/historial')
@login_required
@encargado_required
def historial_admin():
    # Estados finales
    sols = Solicitud.query.filter(Solicitud.estado.in_(['restituido', 'rechazado', 'cancelado'])).all()
    return render_template('enc_sol_historial.html', solicitudes=sols)

# Acción de procesar (se llamará desde los botones)
@encargado_bp.route('/procesar/<int:id>/<estado>', methods=['POST'])
@login_required
@encargado_required
def procesar(id, estado):
    motivo = request.form.get('motivo')
    gestionar_solicitud(id, estado, current_user.id, motivo)
    return redirect(request.referrer) 



### Equipos
@encargado_bp.route('/equipos/administrar')
@login_required
@encargado_required
def administrar_equipos():
    equipos = Equipo.query.all()
    return render_template('enc_equipo_administrar.html', equipos=equipos)


@encargado_bp.route('/equipos/registrar', methods=['GET', 'POST'])
@login_required
@encargado_required
def registrar_equipo():
    if request.method == 'POST':
        registrar_nuevo_equipo(
            request.form.get('nombre'),
            request.form.get('t_min'),
            request.form.get('t_max'),
            request.form.get('id_inv'),
            current_user.id
        )
        return redirect(url_for('encargado.administrar_equipos'))
    return render_template('enc_equipo_registro.html')


@encargado_bp.route('/equipos/cambiar_estado/<int:id>', methods=['POST'])
@login_required
@encargado_required
def cambiar_estado(id):
    
    nuevo_estado = request.form.get('nuevo_estado') == 'True'
    motivo = request.form.get('motivo')
    modificar_disponibilidad(id, nuevo_estado, motivo, current_user.id)
    return redirect(url_for('encargado.administrar_equipos'))



