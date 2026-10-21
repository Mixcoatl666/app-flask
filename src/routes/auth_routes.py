from flask import Blueprint, request, jsonify, session
from models import db
from models.usuario import Usuario

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
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

@bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    usuario = Usuario.query.filter_by(correo=data.get('correo')).first()

    if usuario and usuario.check_password(data.get('password')):
        session['user_id'] = usuario.idusuario
        return jsonify({'message': f'Usuario: {usuario.usuario}, ha iniciado sesión correctamente'}), 200
    else:
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401

@bp.route('/logout', methods=['POST'])
def logout_usuario():
    session.pop('user_id', None)
    return jsonify({'message': 'Usuario ha cerrado sesión correctamente'}), 200

@bp.route('/check-auth', methods=['GET'])
def check_auth():
    user_id = session.get('user_id')

    if user_id:
        user = Usuario.query.get(user_id)
        if user:
            return jsonify({
                'authenticated': True,
                'usuario': user.usuario,
                'user_id': user.idusuario
            }), 200
        else:
            return jsonify({
                'authenticated': False
            }), 401
    else:
        return jsonify({
            'authenticated': False
        }), 401
