# =========================
# IMPORTAR FLASK
# =========================
from flask import (
    Flask,
    render_template,
    request,
    redirect
)

# =========================
# IMPORTAR EXTENSIONES
# =========================
from extensions import (
    db,
    login_manager
)

# =========================
# IMPORTAR BLUEPRINTS
# =========================
from routes.auth_routes import auth_bp
from routes.dashboard_routes import (dashboard_bp)
from routes.historial_routes import (historial_bp)
from routes.calculadora_routes import (calculadora_bp)
from routes.movimiento_routes import (movimiento_bp)

# =========================
# IMPORTAR LOGIN
# =========================
from flask_login import (
    login_required,
    current_user
)

# =========================
# IMPORTAR MODELOS
# =========================
from models.usuario import Usuario
from models.movimiento import (Movimiento)
from models.calculo import Calculo

# =========================
# CREAR APP FLASK
# =========================
app = Flask(__name__)


# =========================
# CONFIGURACIÓN GENERAL
# =========================
# CLAVE SECRETA
app.config['SECRET_KEY'] = (
    'clave_secreta'
)

#BASE DE DATOS SQLITE
#app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'sqlite:///presupuesto.db'

#Render usa PostgreSQL y  PC usa SQLite
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///presupuesto.db'
)

# DESACTIVAR TRACKING
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'
] = False

# =========================
# INICIALIZAR BASE DATOS
# =========================
db.init_app(app)


# =========================
# INICIALIZAR LOGIN
# =========================
login_manager.init_app(app)

# RUTA LOGIN PRINCIPAL
login_manager.login_view = (
    'auth.login'
)

# =========================
# REGISTRAR BLUEPRINTS
# =========================
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(calculadora_bp)
app.register_blueprint(movimiento_bp)

# =========================
# CARGAR USUARIO LOGIN
# =========================
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id)    )


# =========================
# RUTA PRINCIPAL
# =========================
@app.route(
    '/',
    methods=['GET', 'POST']
)
@login_required
def inicio():

    # =========================
    # GUARDAR MOVIMIENTO
    # =========================
    if request.method == 'POST':

        # CAPTURAR DATOS
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        valor = float(request.form['valor'])
        categoria = request.form['categoria']
        metodo_pago = request.form['metodo_pago']
        fecha_manual = request.form['fecha_manual']

        # VALIDAR VALOR
        if valor <= 0:

            return redirect('/')

        # CREAR MOVIMIENTO
        nuevo_movimiento = Movimiento(
            tipo=tipo,
            descripcion=descripcion,
            valor=valor,
            fecha=fecha_manual,
            categoria=categoria,
            metodo_pago=metodo_pago,
            usuario_id=current_user.id
        )

        # GUARDAR EN BD
        db.session.add(nuevo_movimiento)
        db.session.commit()
        return redirect('/')

    # =========================
    # CONSULTAR MOVIMIENTOS
    # =========================
    movimientos_totales = (
        Movimiento.query.filter_by(
            usuario_id=current_user.id
        ).order_by(
            Movimiento.id.desc()
        ).all()
    )

    # ÚLTIMOS 3 MOVIMIENTOS
    movimientos = (
        Movimiento.query.filter_by(
            usuario_id=current_user.id
        ).order_by(
            Movimiento.id.desc()
        ).limit(3).all()
    )

    # =========================
    # VARIABLES FINANCIERAS
    # =========================
    saldo = 0
    total_ingresos = 0
    total_gastos = 0

    # =========================
    # CALCULAR TOTALES
    # =========================
    for movimiento in movimientos_totales:

        # VALIDAR INGRESOS
        if movimiento.tipo == 'Ingreso':
            saldo += movimiento.valor
            total_ingresos += (
                movimiento.valor
            )

        # VALIDAR GASTOS
        else:
            saldo -= movimiento.valor
            total_gastos += (
                movimiento.valor
            )

    # =========================
    # MOSTRAR INDEX
    # =========================
    return render_template(
        'index.html',
        movimientos=movimientos,
        saldo=saldo,
        total_ingresos=total_ingresos,
        total_gastos=total_gastos
    )

# =========================
# CREAR BASE DE DATOS
# =========================
with app.app_context():
    db.create_all()

# =========================
# EJECUTAR APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)