from flask import Blueprint, render_template, request, redirect, url_for
### from database.models import db, Solicitud, Equipo, SolicitudEquipo
from flask_login import current_user, login_required
from datetime import date, timedelta, datetime

from logic_formulario import contar_equipos_activos_usuario, obtener_equipos_disponibles, guardar_nueva_solicitud


usuario_bp = Blueprint('usuario', __name__, url_prefix='/Usuario')


@usuario_bp.route('/Equipos')
@login_required 
def mis_libros():
    return render_template('Equipos.html')



@usuario_bp.route('/Solicitar', methods=['GET', 'POST'])
@login_required 
def solicitar():

    if current_user.condicion_bloqueo != 0:
        return render_template('solicitar.html', bloqueado=True)

    hoy = date.today()
    
    limite_base = 10 if current_user.profesor else 3
    equipos_ya_poseidos = contar_equipos_activos_usuario(current_user.id)
    cupo_disponible = limite_base - equipos_ya_poseidos

    if cupo_disponible <= 0:
        return render_template('solicitar.html', cupo_excedido=True, limite=limite_base)

    ### PASO 1: Selección de fechas
    if request.method == 'GET' and not request.args.get('fecha_inicio'):
        fecha_min = hoy + timedelta(days=2)
        fecha_max = hoy + timedelta(days=7)
        return render_template('solicitar.html', paso=1, fecha_min=fecha_min, fecha_max=fecha_max)

    ### PASO 2: Mostrar equipos
    if request.method == 'GET' and request.args.get('fecha_inicio'):
        f_ini = datetime.strptime(request.args.get('fecha_inicio'), '%Y-%m-%d').date()
        f_fin = datetime.strptime(request.args.get('fecha_fin'), '%Y-%m-%d').date()
        
        equipos = obtener_equipos_disponibles(f_ini, f_fin)
        return render_template('solicitar.html', paso=2, equipos=equipos, f_ini=f_ini, f_fin=f_fin, max_equipos=cupo_disponible)


    ### PASO 3: Guardar 
    if request.method == 'POST':
        equipo_ids = request.form.getlist('equipo_ids')
        motivo = request.form.get('motivo_solicitud')

        if 0 < len(equipo_ids) <= cupo_disponible:
            guardar_nueva_solicitud(
                current_user.id, 
                request.form.get('f_ini'), 
                request.form.get('f_fin'), 
                equipo_ids,
                motivo
            )
    
    return render_template('Solicitar.html')



@usuario_bp.route('/Historial')
@login_required
def historial():
    return render_template('Historial.html')