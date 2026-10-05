import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_cors import CORS

from models import db
from models.nota import Notas
from models.usuario import Usuario

# * Carga las variables definidas en el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

DB_DIALECT = os.environ.get('DB_DIALECT', 'postgresql+psycopg')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = SECRET_KEY

db.init_app(app)

# * Ruta inicial
@app.route('/')
def home():
    return "Hola Flask, que tal? c:"

@app.route('/register', methods=['POST'])
def register_usuario():
    data = request.get_json()

    if Usuario.query.filter_by(correo=data.get('correo')).first() is not None:
        return jsonify({'error': 'El correo ya esta registrado'}), 400

    new_usuario = Usuario(
        usuario=data.get('usuario'),
        correo=data.get('correo')
    )
    new_usuario.set_password(data.get('password'))

    db.session.add(new_usuario)
    db.session.commit()

    return jsonify({
        'message': f'Usuario: {new_usuario.usuario}, registrado correctamente'
    }), 201

@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    usuario = Usuario.query.filter_by(correo=data.get('correo')).first()

    if usuario and usuario.check_password(data.get('password')):
        session['user_id'] = usuario.idusuario
        return jsonify({'message': f'Usuario: {usuario.usuario}, ha iniciado sesión correctamente'}), 200
    else:
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401

@app.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({'authenticated': True}), 200
    else:
        return jsonify({'authenticated': False}), 401

@app.route('/logout', methods=['POST'])
def logout_usuario():
    session.pop('user_id', None)
    return jsonify({'message': 'Usuario ha cerrado sesión correctamente'}), 200

# * Obtenemos todas las notas
@app.route('/notas', methods=['GET'])
def get_notas():
    notas = Notas.query.all()
    
    return jsonify([{
        'idnota': nota.idnota,
        'titulo': nota.titulo,
        'descripcion': nota.descripcion,
        'imagen_url': nota.imagen_url,
        'autor': nota.usuario.usuario,
        'create_at': nota.create_at.strftime('%d-%m-%Y')
    } for nota in notas])

# * Creamos una nueva nota
@app.route('/create-nota', methods=['GET', 'POST'])
def create_nota():
    data = request.get_json()
    new_nota = Notas (
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        imagen_url=data.get('imagen_url'),
        idusuario=session.get('user_id')
    )
    
    db.session.add(new_nota)
    db.session.commit()

    return jsonify({
        'idnota': new_nota.idnota,
        'titulo': new_nota.titulo,
        'descripcion': new_nota.descripcion,
        'imagen_url': new_nota.imagen_url,
        'autor': new_nota.usuario.usuario,
        'create_at': new_nota.create_at.strftime('%d-%m-%Y')
    }), 201

# * Actualizamos una nota
@app.route('/notas/<int:nota_id>', methods=['PUT'])
def update_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    data = request.get_json()
    
    nota.titulo = data['titulo']
    nota.descripcion = data['descripcion']
    nota.imagen_url = data.get('imagen_url')

    db.session.commit()

    return jsonify({
        'idnota': nota.idnota,
        'titulo': nota.titulo,
        'descripcion': nota.descripcion,
        'imagen_url': nota.imagen_url,
        'autor': nota.usuario.usuario,
        'create_at': nota.create_at.strftime('%d-%m-%Y')
    }), 201

# * Vemos una nota en particular
@app.route('/notas/<int:nota_id>')
def view_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    
    return jsonify({
        'idnota': nota.idnota,
        'titulo': nota.titulo,
        'descripcion': nota.descripcion,
        'imagen_url': nota.imagen_url,
        'autor': nota.usuario.usuario,
        'create_at': nota.create_at.strftime('%d-%m-%Y')
    }), 201

# * Eliminamos una nota
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
    app.run(debug=True, port=5001)