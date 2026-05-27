# =========================
# IMPORTACIONES
# =========================

# Importa
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

# Importa herramientas de Flask-Login:
# - login_required: protege rutas para usuarios autenticados
# - current_user: obtiene el usuario actualmente logueado
from flask_login import (
    login_required,
    current_user
)

# Importa la instancia de la base de datos
from extensions import db

# Importa el modelo Calculo
from models.calculo import Calculo


# =========================
# CREACIÓN DEL BLUEPRINT
# =========================

# Se crea un Blueprint llamado 'calculadora'
# para agrupar las rutas relacionadas con la calculadora
calculadora_bp = Blueprint(
    'calculadora',
    __name__
)


# =========================
# CALCULADORA
# =========================

# Ruta principal de la calculadora
# Permite métodos GET y POST
@calculadora_bp.route(
    '/calculadora',
    methods=['GET', 'POST']
)

# Solo usuarios autenticados pueden acceder
@login_required
def calculadora():

    # Si el usuario envía el formulario
    if request.method == 'POST':

        # Obtiene la expresión matemática ingresada
        expresion = request.form[
            'expresion'
        ]

        # Obtiene el resultado calculado
        resultado = request.form[
            'resultado'
        ]

        # Crea un nuevo registro de cálculo
        nuevo_calculo = Calculo(

            # Guarda la expresión matemática
            expresion=expresion,

            # Guarda el resultado obtenido
            resultado=resultado,

            # Relaciona el cálculo con el usuario actual
            usuario_id=current_user.id

        )

        # Agrega el cálculo a la sesión de la base de datos
        db.session.add(
            nuevo_calculo
        )

        # Guarda los cambios en la base de datos
        db.session.commit()

        # Redirecciona nuevamente a la calculadora
        return redirect(
            '/calculadora'
        )

    # Consulta los últimos 10 cálculos
    # realizados por el usuario actual
    calculos = Calculo.query.filter_by(

        usuario_id=current_user.id

    ).order_by(

        # Orden descendente por ID
        # para mostrar primero los más recientes
        # solo muestra los primeros 10 registros
        Calculo.id.desc()

    ).limit(10).all()

    # Renderiza la plantilla calculadora.html
    # enviando la lista de cálculos
    return render_template(

        'calculadora.html',

        calculos=calculos

    )