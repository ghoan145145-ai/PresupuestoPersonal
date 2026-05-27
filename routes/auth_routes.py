# =========================
# IMPORTACIONES
# =========================

#Importa
# - Blueprint: permite organizar rutas en módulos
# - render_template: renderiza archivos HTML
# - request: obtiene datos enviados desde formularios
# - redirect: redirecciona a otra ruta
from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

# Importa funciones de seguridad para contraseñas
#encripta y verifica la contraseña encriptada
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Importa funciones de autenticación de Flask-Login
from flask_login import (
    login_user,
    logout_user,
    login_required
)

# Importa la conexión a la base de datos
from extensions import db

# Importa el modelo Usuario
from models.usuario import Usuario


auth_bp = Blueprint(
    'auth',
    __name__
)


# =========================
# CREACIÓN DEL BLUEPRINT
# =========================

# para agrupar todas las rutas de autenticación
@auth_bp.route(
    '/registro',
    methods=['GET', 'POST']
)

# =========================
# REGISTRO DE USUARIO
# =========================

# Ruta para registrar usuarios
# Acepta métodos GET y POST
def registro():

    if request.method == 'POST':

        #obtener nombre usuario y lo deja en mayuscula
        usuario = request.form[
            'usuario'
        ].upper()

        #para obtener contraseña del formulario
        password = request.form[
            'password'
        ]

        # Busca si el usuario ya existe
        usuario_existente = \
            Usuario.query.filter_by(
                usuario=usuario
            ).first()

        if usuario_existente:
            #si existe mensaje de error
            return render_template(
                'registro.html',
                mensaje_error='El usuario ya existe'
            )

        #encripta la contraseña
        password_encriptada = \
            generate_password_hash(
                password
            )

        #para creacion de usuario
        nuevo_usuario = Usuario(

            usuario=usuario,

            password=password_encriptada

        )

        # Agrega el usuario a la sesión
        db.session.add(
            nuevo_usuario
        )

        # Guarda los cambios en la base de datos
        db.session.commit()

        #Redirecciona al login con mensaje de éxito
        return redirect(
            '/login?exito=1'
        )
    
    # Si es método GET
    # muestra el formulario de registro
    return render_template(
        'registro.html'
    )


# =========================
# LOGIN
# =========================

#ruta para inciiar sesion
@auth_bp.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    # Variables para mensajes
    mensaje_exito = None
    mensaje_error = None

    # Verifica si viene parámetro de éxito
    if request.args.get('exito'):

        mensaje_exito = \
            'Usuario creado correctamente'

    # Si el formulario fue enviado  
    if request.method == 'POST':

        # Obtiene usuario y lo convierte a mayúsculas
        usuario = request.form[
            'usuario'
        ].upper()

        # Obtiene contraseña
        password = request.form[
            'password'
        ]

        # Busca el usuario en la base de datos
        usuario_encontrado = \
            Usuario.query.filter_by(
                usuario=usuario
            ).first()

        # Verifica:Que el usuario exista y contraseña sea correcta
        if usuario_encontrado and \
            check_password_hash(
                usuario_encontrado.password,
                password
            ):

            # Inicia sesión del usuario
            login_user(
                usuario_encontrado
            )

            # Redirecciona a la página principal
            return redirect('/')

        # Mensaje de error si credenciales incorrectas
        else:

            mensaje_error = \
                'Usuario o contraseña incorrectos'

    # Muestra el formulario login
    return render_template(

        'login.html',

        mensaje_exito=mensaje_exito,

        mensaje_error=mensaje_error

    )


# =========================
# LOGOUT
# =========================

# Solo usuarios autenticados pueden acceder
@auth_bp.route('/logout')
@login_required
def logout():
    # Cierra la sesión actual
    logout_user()
    # Redirecciona al login
    return redirect('/login')