from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

# Creamos la instancia acá
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)

    encargado = db.Column(db.Boolean, default=False, nullable=False)
    profesor = db.Column(db.Boolean, default=False, nullable=False)

    condicion_bloqueo = db.Column(db.Integer, default=0, nullable=False)

    # Relaciones
    equipos_registrados = db.relationship(
        "Equipo",
        foreign_keys="Equipo.usuario_registro_id",
        backref="usuario_registro"
    )

    equipos_disponibilidad_cambiada = db.relationship(
        "Equipo",
        foreign_keys="Equipo.usuario_disponibilidad_id",
        backref="usuario_disponibilidad"
    )

    solicitudes = db.relationship(
        "Solicitud",
        foreign_keys="Solicitud.solicitante_id",
        backref="solicitante"
    )

    solicitudes_resueltas = db.relationship(
        "Solicitud",
        foreign_keys="Solicitud.aprobador_id",
        backref="aprobador"
    )

    solicitudes_canceladas = db.relationship(
        "Solicitud",
        foreign_keys="Solicitud.cancelador_id",
        backref="cancelador"
    )


class Equipo(db.Model):
    __tablename__ = "equipo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    tiempo_max = db.Column(db.Integer, nullable=False)
    tiempo_min = db.Column(db.Integer, nullable=False)

    disponible = db.Column(db.Boolean, default=True, nullable=False)

    motivo = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.Date, default=date.today, nullable=False)

    # Usuario que registró el equipo
    usuario_registro_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    # Usuario que cambió manualmente la disponibilidad
    usuario_disponibilidad_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=True
    )


class Solicitud(db.Model):
    __tablename__ = "solicitud"

    id = db.Column(db.Integer, primary_key=True)

    # Usuario que realiza la solicitud
    solicitante_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    # Usuario que aprueba/rechaza
    aprobador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=True
    )

    dias_solicitado = db.Column(db.Integer, nullable=False)

    estado = db.Column(db.String(30), nullable=False, default="pendiente")

    fecha_solicitud = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    fecha_entrega = db.Column(db.Date, nullable=True)

    fecha_devolucion_esperada = db.Column(db.Date, nullable=True)

    fecha_devolucion = db.Column(db.Date, nullable=True)

    cancelado = db.Column(db.Boolean, default=False, nullable=False)

    fecha_cancelacion = db.Column(db.Date, nullable=True)

    motivo_rechazo_cancelacion = db.Column(
        db.String(255),
        nullable=True
    )

    # Usuario que cancela
    cancelador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=True
    )

    notificado = db.Column(db.Boolean, default=False, nullable=False)


class SolicitudEquipo(db.Model):
    """
    Tabla intermedia entre Solicitud y Equipo.

    Permite que una solicitud tenga uno o varios equipos.
    """

    __tablename__ = "solicitud_equipo"

    solicitud_id = db.Column(
        db.Integer,
        db.ForeignKey("solicitud.id"),
        primary_key=True
    )

    equipo_id = db.Column(
        db.Integer,
        db.ForeignKey("equipo.id"),
        primary_key=True
    )
