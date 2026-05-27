#IMPORTANCION SQLAlchemy CREADA EN EXTENSION.PY
from extensions import db
#UserMixin para autenticacion de usuario
from flask_login import UserMixin


#CLASE PRINCIPAL
class Usuario(UserMixin, db.Model):
    #CAMPO ID
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #CAMPO USUARIO
    usuario = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    #CAMPO PASSWORD
    password = db.Column(
    db.String(500),
    nullable=False
    )