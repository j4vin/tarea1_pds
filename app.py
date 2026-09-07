import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from database.models import db, Usuario, Equipo, Solicitud, SolicitudEquipo
from flask_login import LoginManager, login_required
from observability import configure_observability

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tarea1.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-solo-para-desarrollo')

configure_observability(app)

db.init_app(app)

with app.app_context():
    db.create_all()

#-------------------------------------------------------------------------------- IMPORT RUTAS --------------------------------------------------------------------------------
from api.auth import api_auth_bp
from routes.registro import registro_bp
from routes.auth import auth_bp
from routes.usuario import usuario_bp
from routes.encargado import encargado_bp
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Logica del login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from database.models import Usuario
    return Usuario.query.get(int(user_id))


#-------------------------------------------------------------------------------- BLUEPRINTS RUTAS --------------------------------------------------------------------------------
app.register_blueprint(api_auth_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(encargado_bp)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




@app.route('/')
@login_required
def index():
    return redirect(url_for('usuario.equipos'))


if __name__ == "__main__":
    app.run(debug=True)
