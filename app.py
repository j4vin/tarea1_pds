from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from models import db, Usuario, Equipo, Solicitud, SolicitudEquipo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tarea1.db'
app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura'

db.init_app(app)

with app.app_context():
    db.create_all()

#-------------------------------------------------------------------------------- IMPORT RUTAS --------------------------------------------------------------------------------
from api.auth import auth_bp
from routes.registro import registro_bp
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------- BLUEPRINTS RUTAS --------------------------------------------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(registro_bp)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)