# App Flask

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-4169E1)
![Estado](https://img.shields.io/badge/estado-archivado-lightgrey)

> **Proyecto archivado:** ya no está en desarrollo activo. Se publica como proyecto de aprendizaje y referencia.

API REST de ejemplo para gestionar usuarios y notas con Flask, SQLAlchemy y PostgreSQL. Incluye registro, inicio de sesión basado en sesiones y operaciones sobre notas.

## Tecnologías

- Python 3.10 o superior
- Flask y Flask-SQLAlchemy
- PostgreSQL con `psycopg`
- Flask-CORS y `python-dotenv`

## Configuración local

Necesitas Python y una instancia de PostgreSQL accesible.

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install Flask Flask-SQLAlchemy 'psycopg[binary]' python-dotenv Flask-Cors
cp .env.example .env
```

Completa en `.env` las credenciales de PostgreSQL y define un `SECRET_KEY` aleatorio. Puedes generarlo con:

```sh
python -c "import secrets; print(secrets.token_hex(32))"
```

Añade el resultado a `.env` como `SECRET_KEY=...`. **No publiques ni subas `.env` a Git**; el archivo está excluido mediante `.gitignore`.

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `DB_DIALECT` | Dialecto y driver de SQLAlchemy | `postgresql+psycopg` |
| `DB_USER` | Usuario de PostgreSQL | — |
| `DB_PASSWORD` | Contraseña de PostgreSQL | — |
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Base de datos | — |
| `SECRET_KEY` | Clave para firmar las sesiones de Flask | — |
| `PORT` | Puerto HTTP de desarrollo | `5001` |

Las tablas se crean al iniciar la aplicación con `db.create_all()`. `db/tablas.sql` es solo una referencia para la tabla de usuarios, no el esquema completo.

## Ejecutar

Desde la raíz del repositorio, con el entorno virtual activado y `.env` configurado:

```sh
cd src
python3 run.py
```

La API estará disponible por defecto en <http://127.0.0.1:5001>. La variable `PORT` permite cambiar el puerto.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/` | Comprobación básica de la API |
| `POST` | `/register` | Registro de usuario |
| `POST` | `/login` | Inicio de sesión |
| `GET` | `/check-auth` | Estado de autenticación |
| `POST` | `/logout` | Cierre de sesión |
| `GET` | `/notas` | Lista todas las notas |
| `POST` | `/create-nota` | Crea una nota |
| `GET` | `/notas/<nota_id>` | Consulta una nota |
| `PUT` | `/notas/<nota_id>` | Actualiza una nota |
| `DELETE` | `/notas/<nota_id>` | Elimina una nota |
| `POST` | `/notas/favoritos/<nota_id>` | Marca o desmarca una nota como favorita |
| `GET` | `/notas/favoritos` | Lista las notas favoritas del usuario autenticado |

La autenticación usa cookies de sesión. Los clientes frontend deben enviar credenciales al hacer peticiones. Actualmente el indicador de favorito está guardado en la nota, por lo que es global y no independiente por usuario.

## Estructura

```text
src/
├── app.py                 # Configuración y factory create_app()
├── run.py                 # Punto de entrada para desarrollo
├── models/                # Modelos SQLAlchemy
└── routes/                # Blueprints de autenticación y notas
db/
└── tablas.sql             # Referencia parcial del esquema
```
