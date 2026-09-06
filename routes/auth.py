from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from logic_auth import verificar_credenciales

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        usuario = verificar_credenciales(correo, password)
        
        if usuario:
            login_user(usuario)
            return redirect(url_for('index')) ### AQUI esta el redirect
        
        flash('Correo o contraseña incorrectos')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))