# =========================
# IMPORTAR SQLALCHEMY
# =========================
from flask_sqlalchemy import (
    SQLAlchemy
)

# =========================
# IMPORTAR LOGIN MANAGER
# =========================
from flask_login import (
    LoginManager
)

# PERMITE CONECTAR FLASK CON SQLALCHEMY
db = SQLAlchemy()


# =========================
# CREAR LOGIN MANAGER QUE CONTROLA LOGIN Y AUTENTICACION
# =========================
login_manager = LoginManager()