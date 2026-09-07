from database.models import db, Equipo

def registrar_nuevo_equipo(nombre, t_min, t_max, user_id):
    nuevo = Equipo(
        nombre=nombre,
        tiempo_min=int(t_min),
        tiempo_max=int(t_max),
        usuario_registro_id=user_id,
        disponible=True
    )
    db.session.add(nuevo)
    db.session.commit()

def modificar_disponibilidad(equipo_id, nuevo_estado, motivo, user_id):
    equipo = Equipo.query.get(equipo_id)
    if equipo:
        equipo.disponible = nuevo_estado
        equipo.motivo = motivo
        equipo.usuario_disponibilidad_id = user_id
        db.session.commit()