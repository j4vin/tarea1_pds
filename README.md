# Tarea 1
## Integrantes:
- Esteban Becerra
- Javiera Cortés

## Instalar:
pip install virtualenv

## Crear el env:
virtualenv env

## Activar el env:
Windows: .\env\Scripts\activate
Mac/Linux: source venv/bin/activate

## Instalar librerias dentro del env:
pip install [libreria]
pip install -r requirements.txt

# Features en esta rama
### Estructura base
- README.md: Archivo para la documentación inicial del proyecto.
- requirements.txt: Declaración de las librerías y dependencias necesarias para que la aplicación funcione.

### app.py
- Configuración de Flask y conexión a base de datos local SQLite (Tarea1.db) a través de SQLAlchemy.
- Crea las tablas de base de datos automáticamente
- Ruta raíz que llama a index.

### instance/
- Contiene archivo físico de la base de datos (Tarea1.db)-

### static/css
- main.css: Archivo con estilos mínimos.

### templates/
- base.html: Plantilla principal que armaba la estructura básica del HTML (el head y el body) y conecta la hoja de estilos.
- index.html: Vista inicial sencilla que hereda de base.html.
