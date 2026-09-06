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
- Creación automática de las tablas de la base de datos.
- Registro de los blueprints de autenticación y registro de usuarios.
- Ruta raíz que renderiza la vista inicial.

### Registro de usuarios

- Formulario de creación de cuenta disponible en la ruta `/registro`.
- Validación en tiempo real de correos institucionales con los dominios `@alumno.usm.cl` y `@profesor.usm.cl`.
- Comprobación de que la contraseña y su confirmación coincidan antes de habilitar el registro.
- Detección automática del nombre y del tipo de usuario (alumno o profesor) a partir del correo institucional.
- Verificación de correos previamente registrados para evitar cuentas duplicadas.
- Almacenamiento seguro de contraseñas mediante hash.

### api/

- auth.py: Contiene la validación del formato de correo, la extracción de datos del usuario y el endpoint `/api/validar_correo`.

### routes/

- registro.py: Procesa la creación de cuentas, valida los datos y guarda los nuevos usuarios en la base de datos.

### models.py

- Define los modelos `Usuario`, `Equipo`, `Solicitud` y `SolicitudEquipo`.
- Configura las relaciones entre usuarios, equipos y solicitudes.

### instance/

- Contiene el archivo físico de la base de datos (`Tarea1.db`).

### static/css/

- main.css: Archivo con estilos mínimos.

### templates/

- base.html: Plantilla principal que define la estructura básica del HTML y conecta la hoja de estilos.
- index.html: Vista inicial sencilla que hereda de base.html.
- registro.html: Formulario de registro con validación interactiva del correo y de las contraseñas.

### templates/
- base.html: Plantilla principal que armaba la estructura básica del HTML (el head y el body) y conecta la hoja de estilos.
- index.html: Vista inicial sencilla que hereda de base.html.
