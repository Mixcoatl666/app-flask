from models import db

# * Definimos el modelo de Notas
class Notas(db.Model):
    idnota = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True) 
    create_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Nota {self.titulo}>"