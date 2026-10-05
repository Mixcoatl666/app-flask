from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class Usuario(db.Model):
    idusuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    notas = db.relationship('Notas', backref='usuario', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'