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