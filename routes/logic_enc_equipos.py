from flask import current_app
from database.models import db, Equipo

def registrar_nuevo_equipo(nombre, t_min, t_max, user_id):
    nuevo = Equipo(
        nombre=nombre,
        tiempo_min=int(t_min),
        tiempo_max=int(t_max),
        usuario_registro_id=user_id,
        disponible=True
    )
    try:
        db.session.add(nuevo)
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "equipment_registration_failed manager_id=%s",
            user_id,
        )
        raise

    current_app.logger.info(
        "equipment_registered equipment_id=%s manager_id=%s available=True",
        nuevo.id,
        user_id,
    )
    return nuevo

def modificar_disponibilidad(equipo_id, nuevo_estado, motivo, user_id):
    try:
        equipo = Equipo.query.get(equipo_id)
    except Exception:
        current_app.logger.exception(
            "equipment_lookup_failed equipment_id=%s manager_id=%s",
            equipo_id,
            user_id,
        )
        raise
    if not equipo:
        current_app.logger.warning(
            "equipment_availability_change_rejected equipment_id=%s manager_id=%s reason=not_found",
            equipo_id,
            user_id,
        )
        return False

    estado_anterior = equipo.disponible
    try:
        equipo.disponible = nuevo_estado
        equipo.motivo = motivo
        equipo.usuario_disponibilidad_id = user_id
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "equipment_availability_change_failed equipment_id=%s manager_id=%s",
            equipo_id,
            user_id,
        )
        raise

    current_app.logger.info(
        "equipment_availability_changed equipment_id=%s manager_id=%s previous=%s current=%s",
        equipo_id,
        user_id,
        estado_anterior,
        nuevo_estado,
    )
    return True
