from database.models import db, Solicitud
from datetime import date
from flask import current_app

def gestionar_solicitud(sol_id, nuevo_estado, admin_id, motivo=None):
    try:
        sol = Solicitud.query.get(sol_id)
    except Exception:
        current_app.logger.exception(
            "loan_lookup_failed request_id=%s manager_id=%s",
            sol_id,
            admin_id,
        )
        raise
    if not sol:
        current_app.logger.warning(
            "loan_state_change_rejected request_id=%s manager_id=%s reason=not_found",
            sol_id,
            admin_id,
        )
        return False

    estado_anterior = sol.estado

    if nuevo_estado == 'aprobado':
        sol.estado = 'aprobado'
        sol.aprobador_id = admin_id
    
    elif nuevo_estado == 'rechazado':
        sol.estado = 'rechazado'
        sol.aprobador_id = admin_id
        sol.motivo_rechazo_cancelacion = motivo
    
    elif nuevo_estado == 'en posesion':
        sol.estado = 'en posesion'
        sol.fecha_entrega = date.today()
    
    elif nuevo_estado == 'restituido':
        sol.estado = 'restituido'
        sol.fecha_devolucion = date.today()

    else:
        current_app.logger.warning(
            "loan_state_change_rejected request_id=%s manager_id=%s reason=invalid_state requested_state=%s",
            sol_id,
            admin_id,
            nuevo_estado,
        )
        return False

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "loan_state_change_failed request_id=%s manager_id=%s previous_state=%s requested_state=%s",
            sol_id,
            admin_id,
            estado_anterior,
            nuevo_estado,
        )
        raise

    current_app.logger.info(
        "loan_state_changed request_id=%s manager_id=%s previous_state=%s current_state=%s",
        sol_id,
        admin_id,
        estado_anterior,
        nuevo_estado,
    )
    return True

def obtener_solicitudes_progreso_ordenadas():
    estados_visibles = ['atrasado', 'aprobado', 'en posesion']
    sols = Solicitud.query.filter(Solicitud.estado.in_(estados_visibles)).all()

    prioridad = {
        'atrasado': 0,
        'aprobado': 1,
        'en posesion': 2
    }

    return sorted(sols, key=lambda x: prioridad.get(x.estado.lower(), 99))
