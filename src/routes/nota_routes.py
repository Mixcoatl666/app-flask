from flask import Blueprint, request, jsonify, session
from models import db
from models.nota import Notas

bp = Blueprint('notas', __name__)

# * Vemos una nota en particular
@bp.route('/notas/<int:nota_id>')
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

# * Obtenemos todas las notas
@bp.route('/notas', methods=['GET'])
def get_notas():
    notas = Notas.query.all()

    return jsonify([{
        'idnota': nota.idnota,
        'titulo': nota.titulo,
        'descripcion': nota.descripcion,
        'imagen_url': nota.imagen_url,
        'autor': nota.usuario.usuario,
        'create_at': nota.create_at.strftime('%d-%m-%Y'),
        'user_id': nota.idusuario
    } for nota in notas])

# * Creamos una nueva nota
@bp.route('/create-nota', methods=['GET', 'POST'])
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
@bp.route('/notas/<int:nota_id>', methods=['PUT'])
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

# * Eliminamos una nota
@bp.route('/notas/<int:nota_id>', methods=['DELETE'])
def delete_nota(nota_id):
    if 'user_id' not in session:
        return jsonify({'message': 'No autorizado'}), 401

    nota = Notas.query.get_or_404(nota_id)

    if nota.idusuario != session['user_id']:
        return jsonify({'message': 'No autorizado para eliminar esta nota'}), 403

    try:
        db.session.delete(nota)
        db.session.commit()
        return jsonify({'message': 'Nota eliminada con exito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar el articulo', 'error': str(e)})

# * Marcamos o desmarcamos una nota como favorita
@bp.route('/notas/favoritos/<int:nota_id>', methods=['POST'])
def toggle_favoritos(nota_id):
    data = request.get_json()
    is_favorite = data.get('is_favorite')

    nota = Notas.query.get_or_404(nota_id)
    nota.is_favorite = is_favorite

    db.session.commit()

    return jsonify({ "message": "Añadido a favoritos" if is_favorite else "Eliminado de favoritos" }), 201

# * Filtro para traer favoritos
@bp.route('/notas/favoritos', methods=['GET'])
def get_favoritos():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': 'El usuario no está autenticado'}), 401

    notas_favoritas = Notas.query.filter_by(
        idusuario=user_id,
        is_favorite=True
    ).all()
    notas_list = [
        {
            'idnota': nota.idnota,
            'titulo': nota.titulo,
            'descripcion': nota.descripcion,
            'autor': nota.usuario.usuario,
            'imagen_url': nota.imagen_url,
            'is_favorite': nota.is_favorite,
            'create_at': nota.create_at.strftime('%d-%m-%Y')
        } for nota in notas_favoritas
    ]

    return jsonify(notas_list), 200
