import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# * Carga las variables definidas en el archivo .env
load_dotenv()

app = Flask(__name__)

DB_DIALECT = os.environ.get('DB_DIALECT', 'postgresql+psycopg')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# * Definimos el modelo de Notas
class Notas(db.Model):
    idnota = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Nota {self.titulo}>"

# * Ruta inicial
@app.route('/')
def home():
    return "Hola Flask, que tal? c:"

# * Obtenemos todas las notas
@app.route('/notas', methods=['GET'])
def get_notas():
    notas = Notas.query.all()
    
    return jsonify([{
        'idnota': nota.idnota,
        'titulo': nota.titulo,
        'descripcion': nota.descripcion,
        'create_at': nota.create_at
    } for nota in notas])

# * Creamos una nueva nota
@app.route('/create-nota', methods=['GET', 'POST'])
def create_nota():
    data = request.get_json()
    new_nota = Notas (
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion') 
    )
    
    db.session.add(new_nota)
    db.session.commit()

    return jsonify({
        'idnota': new_nota.idnota,
        'titulo': new_nota.titulo
    }), 201

# * Actualizamos una nota
@app.route('/notas/<int:nota_id>', methods=['PUT'])
def update_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    data = request.get_json()
    
    nota.titulo = data['titulo']
    nota.descripcion = data['descripcion']

    db.session.commit()

    return jsonify({
        'idnota': nota.idnota,
        'titulo': nota.titulo
    }), 201

# * Vemos una nota en particular
@app.route('/notas/<int:nota_id>')
def view_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    
    return jsonify({
        'idnota': nota.idnota,
        'titulo': nota.titulo
    }), 201

@app.route('/notas/<int:nota_id>', methods=['DELETE'])
def delete_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)

    db.session.delete(nota)
    db.session.commit()

    return jsonify({
        'message': f'Nota {nota_id} eliminada correctamente'
    }), 200

@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        return f"Articulo creado: {title}, Contenido: {content}"
    return '''
        <form method='POST' action="create-article">
            <label for='title'>Título del artículo:</label><br>
            <input type='text' id='title' name='title'><br><br>

            <label for='content'>Contenido del artículo:</label><br>
            <textarea id='content' name='content'></textarea><br><br>

            <input type='submit' id='title' value='Crear Artículo'>
        </form>
    '''

@app.route('/article/<int:article_id>')
def view_article(article_id):
    return f"Estas viendo el articulo numero: {article_id}"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)