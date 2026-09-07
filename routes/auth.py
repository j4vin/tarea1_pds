from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .logic_auth import verificar_credenciales

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        usuario = verificar_credenciales(correo, password)
        
        if usuario:
            login_user(usuario)
            current_app.logger.info("user_login_succeeded user_id=%s", usuario.id)
            return redirect(url_for('index')) ### AQUI esta el redirect
        
        current_app.logger.warning("user_login_failed")
        flash('Correo o contraseña incorrectos')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    current_app.logger.info("user_logout_succeeded user_id=%s", user_id)
    return redirect(url_for('auth.login'))
