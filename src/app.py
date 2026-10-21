import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from models import db

# * Carga las variables definidas en el archivo .env
load_dotenv()

DB_DIALECT = os.environ.get('DB_DIALECT', 'postgresql+psycopg')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')

def create_app():
    app = Flask(__name__)
    
    CORS(app, supports_credentials=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)

    from routes import auth_routes, nota_routes

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(nota_routes.bp)

    # * Ruta inicial
    @app.route('/')
    def home():
        return "Hola Flask, que tal? c:"

    with app.app_context():
        db.create_all()

    return app
