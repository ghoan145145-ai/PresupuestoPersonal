# =========================
# IMPORTACIONES
# =========================

# Importa herramientas de Flask:
from flask import (
    Blueprint,
    render_template,
    request
)

# Importa herramientas de Flask-Logino
from flask_login import (
    login_required,
    current_user
)

# Importa el modelo Movimiento
from models.movimiento import Movimiento


# =========================
# CREACIÓN DEL BLUEPRINT
# =========================

# Blueprint encargado de las rutas del dashboard
dashboard_bp = Blueprint(
    'dashboard',
    __name__
)


# =========================
# DASHBOARD
# =========================

# Ruta principal del dashboard
@dashboard_bp.route('/dashboard')

# Solo usuarios autenticados pueden acceder
@login_required
def dashboard():

    # =========================
    # OBTENER FILTROS DESDE URL
    # =========================

    # Obtiene el tipo de movimiento
    # (Ingreso o Gasto)
    tipo = request.args.get('tipo')

    # Obtiene categoría
    categoria = request.args.get(
        'categoria'
    )

    # Obtiene método de pago
    metodo_pago = request.args.get(
        'metodo_pago'
    )

    # Obtiene fecha inicial
    fecha_inicio = request.args.get(
        'fecha_inicio'
    )

    # Obtiene fecha final
    fecha_fin = request.args.get(
        'fecha_fin'
    )

    # =========================
    # CONSULTA BASE
    # =========================

    # Consulta movimientos del usuario actual
    movimientos = Movimiento.query.filter_by(
        usuario_id=current_user.id
    )

    # =========================
    # FILTRO POR TIPO
    # =========================

    if tipo:

        movimientos = movimientos.filter_by(
            tipo=tipo
        )

    # =========================
    # FILTRO POR CATEGORÍA
    # =========================

    if categoria:

        movimientos = movimientos.filter(
            Movimiento.categoria.ilike(
                f"%{categoria}%"
            )
        )

    # =========================
    # FILTRO POR MÉTODO DE PAGO
    # =========================

    if metodo_pago:

        movimientos = movimientos.filter_by(
            metodo_pago=metodo_pago
        )

    # =========================
    # FILTRO POR FECHA INICIAL
    # =========================

    if fecha_inicio:

        movimientos = movimientos.filter(
            Movimiento.fecha >= fecha_inicio
        )

    # =========================
    # FILTRO POR FECHA FINAL
    # =========================

    if fecha_fin:

        movimientos = movimientos.filter(
            Movimiento.fecha <= fecha_fin
        )

    # Ejecuta la consulta
    movimientos = movimientos.all()

    # =========================
    # VARIABLES GENERALES
    # =========================

    # Total de ingresos y total de gastos
    total_ingresos = 0
    total_gastos = 0

    # =========================
    # CATEGORÍAS DE GASTOS
    # =========================

    categorias_gastos = {

        "Comida": 0,
        "Transporte": 0,
        "Estudio": 0,
        "Salud": 0,
        "Ocio": 0,
        "Servicios": 0,
        "Ahorro": 0

    }

    # =========================
    # CATEGORÍAS DE INGRESOS
    # =========================

    categorias_ingresos = {

        "Salario": 0,
        "Freelance": 0,
        "Ventas": 0,
        "Inversiones": 0,
        "Bonos": 0,
        "Otros": 0

    }

    # =========================
    # MÉTODOS DE PAGO
    # =========================

    metodos_pago = {

        "Efectivo": 0,
        "Nequi": 0,
        "Daviplata": 0,
        "Tarjeta": 0,
        "Transferencia": 0

    }

    # =========================
    # RECORRER MOVIMIENTOS
    # =========================

    for movimiento in movimientos:

        # Verifica si el método de pago existe
        if movimiento.metodo_pago \
            in metodos_pago:

            # Suma el valor al método correspondiente
            metodos_pago[
                movimiento.metodo_pago
            ] += movimiento.valor

        # =========================
        # SI ES INGRESO
        # =========================

        if movimiento.tipo == 'Ingreso':

            # Suma ingresos
            total_ingresos += \
                movimiento.valor

            # Suma valores por categoría
            if movimiento.categoria \
                in categorias_ingresos:

                categorias_ingresos[
                    movimiento.categoria
                ] += movimiento.valor

        # =========================
        # SI ES GASTO
        # =========================

        else:

            # Suma gastos
            total_gastos += \
                movimiento.valor

            # Suma gastos por categoría
            if movimiento.categoria \
                in categorias_gastos:

                categorias_gastos[
                    movimiento.categoria
                ] += movimiento.valor

    # =========================
    # DATOS PARA GRÁFICAS
    # =========================

    # Lista de fechas y valores
    fechas = []
    valores = []

    # Recorre movimientos
    for movimiento in movimientos:

        # Guarda fecha
        fechas.append(
            movimiento.fecha
        )

        # Si es ingreso agrega valor positivo
        if movimiento.tipo == 'Ingreso':

            valores.append(
                movimiento.valor
            )

        # Si es gasto agrega valor negativo
        else:

            valores.append(
                -movimiento.valor
            )

    # =========================
    # BALANCE NETO
    # =========================

    # Calcula ingresos menos gastos
    balance_neto = total_ingresos - total_gastos

    # =========================
    # CANTIDAD DE MOVIMIENTOS
    # =========================

    cantidad_movimientos = len(movimientos)

    # =========================
    # MAYOR GASTO E INGRESO
    # =========================

    mayor_gasto = 0
    mayor_ingreso = 0

    # Recorre movimientos
    for movimiento in movimientos:

        # Si es gasto
        if movimiento.tipo == 'Gasto':

            # Verifica si es el gasto más alto
            if movimiento.valor > mayor_gasto:

                mayor_gasto = movimiento.valor

        # Si es ingreso
        else:

            # Verifica si es el ingreso más alto
            if movimiento.valor > mayor_ingreso:

                mayor_ingreso = movimiento.valor

    # =========================
    # RENDERIZAR DASHBOARD
    # =========================

    return render_template(

        'dashboard.html',

        # Totales generales
        total_ingresos=total_ingresos,
        total_gastos=total_gastos,
        balance_neto=balance_neto,

        # Estadísticas
        cantidad_movimientos=cantidad_movimientos,

        mayor_gasto=mayor_gasto,
        mayor_ingreso=mayor_ingreso,

        # Categorías
        categorias_gastos=categorias_gastos,
        categorias_ingresos=categorias_ingresos,

        # Datos para gráficas
        fechas=fechas,
        valores=valores,

        # Métodos de pago
        metodos_pago=metodos_pago

    )