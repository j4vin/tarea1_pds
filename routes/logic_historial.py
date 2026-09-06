from datetime import date
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
    solicitud = Solicitud.query.get(solicitud_id)
    # Validamos que el usuario sea el dueño y la solicitud sea elegible
    if solicitud and solicitud.solicitante_id == user_id:
        if solicitud.estado.lower() in ['pendiente', 'aprobado', 'en posesion']:
            solicitud.estado = 'cancelado'
            solicitud.cancelado = True
            solicitud.fecha_cancelacion = date.today()
            solicitud.cancelador_id = user_id
            solicitud.motivo_rechazo_cancelacion = motivo
            db.session.commit()
            return True
    return False