# Importa herramientas de Flask:
from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

# IMPORTAR SEGURIDAD LOGIN
from flask_login import (
    login_required,
    current_user
)

# IMPORTAR BASE DE DATOS
from extensions import db

# IMPORTAR MODELO MOVIMIENTO
from models.movimiento import Movimiento


# =========================
# CREAR BLUEPRINT MOVIMIENTO
# =========================

movimiento_bp = Blueprint(
    'movimiento',
    __name__
)


# =========================
# ELIMINAR MOVIMIENTO
# =========================

@movimiento_bp.route(
    '/eliminar/<int:id>/<origen>'
)
@login_required
def eliminar(id, origen):

    # BUSCAR MOVIMIENTO
    movimiento = Movimiento.query.get(id)

    # VALIDAR QUE EL MOVIMIENTO PERTENEZCA AL USUARIO
    if movimiento.usuario_id == current_user.id:

        # ELIMINAR MOVIMIENTO Y GUARDA CAMBIOS
        db.session.delete(movimiento)
        db.session.commit()

    # VALIDAR ORIGEN PARA REDIRECCIÓN
    if origen == 'historial':

        return redirect('/historial')

    # REDIRECCIÓN PRINCIPAL
    return redirect('/')


# =========================
# EDITAR MOVIMIENTO
# =========================

@movimiento_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
@login_required
def editar(id):

    # BUSCAR MOVIMIENTO
    movimiento = Movimiento.query.get(id)

    # VALIDAR QUE EL MOVIMIENTO SEA DEL USUARIO ACTUAL
    if movimiento.usuario_id != current_user.id:

        return redirect('/historial')

    # =========================
    # ACTUALIZAR MOVIMIENTO
    # =========================

    if request.method == 'POST':

        # ACTUALIZAR TIPO
        movimiento.tipo = request.form['tipo']

        # ACTUALIZAR DESCRIPCIÓN
        movimiento.descripcion = request.form[
            'descripcion'
        ]

        # ACTUALIZAR VALOR
        movimiento.valor = float(
            request.form['valor']
        )

        # ACTUALIZAR FECHA
        movimiento.fecha = request.form[
            'fecha'
        ]

        # ACTUALIZAR CATEGORÍA
        movimiento.categoria = request.form[
            'categoria'
        ]

        # ACTUALIZAR MÉTODO PAGO
        movimiento.metodo_pago = request.form[
            'metodo_pago'
        ]

        # GUARDAR CAMBIOS Y REDIRECCIONA HISTORIAL
        db.session.commit()
        return redirect('/historial')

    # MOSTRAR FORMULARIO EDITAR
    return render_template(

        'editar.html',

        movimiento=movimiento

    )