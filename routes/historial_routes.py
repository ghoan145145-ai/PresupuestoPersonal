# Importa herramientas de Flask:
from flask import (
    Blueprint,
    render_template,
    request,
    send_file
)

# IMPORTAR SEGURIDAD DE LOGIN
from flask_login import (
    login_required,
    current_user
)

# IMPORTAR MODELO MOVIMIENTO
from models.movimiento import Movimiento

# LIBRERÍA PARA CREAR ARCHIVOS EXCEL
import openpyxl

# LIBRERÍA PARA MANEJO EN MEMORIA
from io import BytesIO


# =========================
# CREAR BLUEPRINT HISTORIAL
# =========================

historial_bp = Blueprint(
    'historial',
    __name__
)


# =========================
# HISTORIAL DE MOVIMIENTOS
# =========================

@historial_bp.route('/historial')
@login_required
def historial():

    # OBTENER NÚMERO DE PÁGINA
    pagina = request.args.get(
        'pagina',
        1,
        type=int
    )

    # OBTENER FILTROS DEL FORMULARIO
    tipo = request.args.get('tipo')
    categoria = request.args.get('categoria')
    metodo_pago = request.args.get('metodo_pago')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # CONSULTAR MOVIMIENTOS DEL USUARIO ACTUAL
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
    # FILTRO POR MÉTODO PAGO
    # =========================

    if metodo_pago:

        movimientos = movimientos.filter(
            Movimiento.metodo_pago.ilike(
                f"%{metodo_pago}%"
            )
        )

    # =========================
    # FILTRO FECHA INICIO
    # =========================

    if fecha_inicio:

        movimientos = movimientos.filter(
            Movimiento.fecha >= fecha_inicio
        )

    # =========================
    # FILTRO FECHA FIN
    # =========================

    if fecha_fin:

        movimientos = movimientos.filter(
            Movimiento.fecha <= fecha_fin
        )

    # =========================
    # ORDENAR Y PAGINAR
    # =========================

    movimientos = movimientos.order_by(
        Movimiento.id.desc()
    ).paginate(
        page=pagina,
        per_page=10
    )

    # ENVIAR DATOS AL HTML
    return render_template(

        'historial.html',

        movimientos=movimientos

    )

# =========================
# EXPORTAR MOVIMIENTOS EXCEL
# =========================

@historial_bp.route('/exportar_excel')
@login_required
def exportar_excel():

    # CONSULTAR MOVIMIENTOS DEL USUARIO ACTUAL
    movimientos = Movimiento.query.filter_by(
        usuario_id=current_user.id
    ).all()

    # CREAR ARCHIVO EXCEL
    archivo = openpyxl.Workbook()

    # CREAR HOJA ACTIVA
    hoja = archivo.active

    # ASIGNAR NOMBRE HOJA
    hoja.title = "Movimientos"

    # =========================
    # CREAR ENCABEZADOS
    # =========================

    encabezados = [
        "Tipo",
        "Descripción",
        "Valor",
        "Fecha",
        "Categoría",
        "Método de Pago"
    ]

    # AGREGAR ENCABEZADOS
    hoja.append(encabezados)

    # =========================
    # AGREGAR MOVIMIENTOS
    # =========================

    for movimiento in movimientos:

        hoja.append([
            movimiento.tipo,
            movimiento.descripcion,
            movimiento.valor,
            movimiento.fecha,
            movimiento.categoria,
            movimiento.metodo_pago
        ])

    # =========================
    # CREAR ARCHIVO EN MEMORIA
    # =========================

    excel = BytesIO()
    archivo.save(excel)
    excel.seek(0)

    # =========================
    # DESCARGAR ARCHIVO
    # =========================

    return send_file(
        excel,
        download_name='movimientos.xlsx',
        as_attachment=True
    )