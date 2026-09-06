from datetime import timedelta, datetime
from database.models import db, Equipo, Solicitud, SolicitudEquipo


def contar_equipos_activos_usuario(user_id):
    
    estados_activos = ['pendiente', 'aprobado', 'en posesion', 'atrasado']
    
    total = db.session.query(SolicitudEquipo).join(Solicitud).filter(
        Solicitud.solicitante_id == user_id,
        Solicitud.estado.in_(estados_activos)
    ).count()
    
    return total

def obtener_equipos_disponibles(f_ini, f_fin):

    # Buffer de la nueva solicitud (+/- 1 día)
    busqueda_ini = f_ini - timedelta(days=1)
    busqueda_fin = f_fin + timedelta(days=1)

    estados_intermedios = ['aprobado', 'en posesion', 'atrasado']
    solicitudes_activas = Solicitud.query.filter(Solicitud.estado.in_(estados_intermedios)).all()

    equipos_ocupados_ids = []
    for sol in solicitudes_activas:
        sol_ini_buffer = sol.fecha_entrega - timedelta(days=1)
        sol_fin_buffer = sol.fecha_devolucion_esperada + timedelta(days=1)

        if sol_ini_buffer <= busqueda_fin and sol_fin_buffer >= busqueda_ini:
            vinculos = SolicitudEquipo.query.filter_by(solicitud_id=sol.id).all()
            for v in vinculos:
                equipos_ocupados_ids.append(v.equipo_id)

    return Equipo.query.filter(~Equipo.id.in_(equipos_ocupados_ids)).all()



def guardar_nueva_solicitud(user_id, f_ini_str, f_fin_str, equipo_ids, motivo):
    d_ini = datetime.strptime(f_ini_str, '%Y-%m-%d').date()
    d_fin = datetime.strptime(f_fin_str, '%Y-%m-%d').date()
    
    nueva_sol = Solicitud(
        solicitante_id=user_id,
        dias_solicitado=(d_fin - d_ini).days,
        fecha_entrega=d_ini,
        fecha_devolucion_esperada=d_fin,
        estado="pendiente",
        motivo_solicitud=motivo
    )
    db.session.add(nueva_sol)
    db.session.flush()

    for eid in equipo_ids:
        nueva_relacion = SolicitudEquipo(solicitud_id=nueva_sol.id, equipo_id=int(eid))
        db.session.add(nueva_relacion)

    db.session.commit()