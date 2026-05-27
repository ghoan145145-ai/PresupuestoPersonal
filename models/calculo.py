#IMPORTANCION SQLAlchemy CREADA EN EXTENSION.PY
from extensions import db

#CLASE PRINCIPAL
class Calculo(db.Model):
    #IDENTIFICADOR
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #ALMACENA OPERACION
    expresion = db.Column(
        db.String(100),
        nullable=False
    )
    #GUARDADO DE RESULTADO
    resultado = db.Column(
        db.String(100),
        nullable=False
    )
    #CADA CALCULO PARA CADA USUARIO
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )