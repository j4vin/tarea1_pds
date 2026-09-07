from datetime import date
from flask import current_app
from database.models import db, Solicitud

def obtener_historial_ordenado(user_id):
    solicitudes = Solicitud.query.filter_by(solicitante_id=user_id).all()

    ### orden del filtrado
    orden_prioridad = {
        'atrasado': 0,
        'pendiente': 1,
        'aprobado': 2,
        'en posesion': 3,
        'restituido': 4,
        'rechazado': 5,
        'cancelado': 5
    }
    return sorted(solicitudes, key=lambda x: orden_prioridad.get(x.estado.lower(), 99))

def procesar_cancelacion(solicitud_id, user_id, motivo):
    try:
        solicitud = Solicitud.query.get(solicitud_id)
    except Exception:
        current_app.logger.exception(
            "loan_lookup_failed request_id=%s user_id=%s",
            solicitud_id,
            user_id,
        )
        raise
    if not solicitud:
        current_app.logger.warning(
            "loan_cancellation_rejected request_id=%s user_id=%s reason=not_found",
            solicitud_id,
            user_id,
        )
        return False

    if solicitud.solicitante_id != user_id:
        current_app.logger.warning(
            "loan_cancellation_rejected request_id=%s user_id=%s reason=not_owner",
            solicitud_id,
            user_id,
        )
        return False

    if solicitud.estado.lower() not in ['pendiente', 'aprobado', 'en posesion']:
        current_app.logger.warning(
            "loan_cancellation_rejected request_id=%s user_id=%s reason=invalid_state state=%s",
            solicitud_id,
            user_id,
            solicitud.estado,
        )
        return False

    estado_anterior = solicitud.estado
    try:
        solicitud.estado = 'cancelado'
        solicitud.cancelado = True
        solicitud.fecha_cancelacion = date.today()
        solicitud.cancelador_id = user_id
        solicitud.motivo_rechazo_cancelacion = motivo
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "loan_cancellation_failed request_id=%s user_id=%s",
            solicitud_id,
            user_id,
        )
        raise

    current_app.logger.info(
        "loan_cancelled request_id=%s user_id=%s previous_state=%s",
        solicitud_id,
        user_id,
        estado_anterior,
    )
    return True
