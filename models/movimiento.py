#IMPORTANCION SQLAlchemy CREADA EN EXTENSION.PY
from extensions import db

#CLASE PRINCIPAL
class Movimiento(db.Model):
    #IDENTIFICADOR
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #DEFINE INGRESO O GASTO
    tipo = db.Column(
        db.String(20),
        nullable=False
    )
    #DETALLE DESCRIPCION
    descripcion = db.Column(
        db.String(100),
        nullable=False
    )
    #ALMACENAR VALOR
    valor = db.Column(
        db.Float,
        nullable=False
    )
    #ALMACENA FECHA 
    fecha = db.Column(
        db.String(50),
        nullable=False
    )
    #PARA CLASIFICAR MOVIMIENTO
    categoria = db.Column(
        db.String(50),
        nullable=False
    )
    #MEDIO DE PAGO UTILIZADO
    metodo_pago = db.Column(
        db.String(50),
        nullable=False
    )
    #RELACION CADA MOVIMIENTO CON CADA USUARIO
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )