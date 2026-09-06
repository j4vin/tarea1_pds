from database.models import Solicitud
from datetime import date

def obtener_equipos_en_posesion(user_id):
    solicitudes = Solicitud.query.filter(
        Solicitud.solicitante_id == user_id,
        Solicitud.estado.in_(['en posesion', 'atrasado'])
    ).all()
    
    hoy = date.today()
    resultado = []

    for sol in solicitudes:
        
        for vinculo in sol.solicitud_equipos:
            resultado.append({
                'nombre': vinculo.equipo.nombre,
                'fecha_limite': sol.fecha_devolucion_esperada,
                'atrasado': sol.estado.lower() == 'atrasado'
            })
            
    return resultado