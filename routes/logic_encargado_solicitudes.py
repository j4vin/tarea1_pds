from database.models import db, Solicitud
from datetime import date

def gestionar_solicitud(sol_id, nuevo_estado, admin_id, motivo=None):
    sol = Solicitud.query.get(sol_id)
    if not sol: return False

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

    db.session.commit()
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