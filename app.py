from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from database.models import db, Usuario, Equipo, Solicitud, SolicitudEquipo
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tarea1.db'
app.config['SECRET_KEY'] = 'Esta_Es_Una_Clave_HEHEHE_CAMBIABLE_BTW'

db.init_app(app)

with app.app_context():
    db.create_all()

#-------------------------------------------------------------------------------- IMPORT RUTAS --------------------------------------------------------------------------------
from api.auth import api_auth_bp
from routes.registro import registro_bp
from routes.auth import auth_bp
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
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




@app.route('/')
def index():
    return render_template(url_for('auth.login'))


if __name__ == "__main__":
    app.run(debug=True)