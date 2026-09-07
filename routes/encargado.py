from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from utils import encargado_required
from database.models import Solicitud
from logic_encargado_solicitudes import gestionar_solicitud


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
    # Estados intermedios para el admin
    sols = Solicitud.query.filter(Solicitud.estado.in_(['aprobado', 'en posesion', 'atrasado'])).all()
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



