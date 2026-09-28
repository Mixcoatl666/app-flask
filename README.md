# App Flask

API en Flask con SQLAlchemy para gestionar **notas** y **usuarios** (registro e inicio de sesión), usando PostgreSQL como base de datos.

## Estructura del proyecto

```
app-flask/
├── db/
│   └── tablas.sql        # Script SQL de referencia para crear la tabla de usuarios
├── src/
│   ├── app.py             # Punto de entrada de la aplicación (rutas de Flask)
│   └── models/
│       ├── __init__.py    # Instancia de SQLAlchemy (db)
│       ├── nota.py         # Modelo Notas
│       └── usuario.py      # Modelo Usuario (con hash de contraseña)
├── .env                    # Variables de entorno (NO se sube a git)
└── .env.example            # Plantilla de variables de entorno
```

## Requisitos

* Python 3.10+
* Una base de datos PostgreSQL accesible

## Crear el entorno virtual

```sh
python3 -m venv venv
```

## Activarlo en macOS o Linux

Desde la carpeta del proyecto:

```sh
source venv/bin/activate
```

Cuando está activo, verás `(venv)` al inicio de la línea de comandos.

## Instalar dependencias

```sh
python -m pip install Flask Flask-SQLAlchemy psycopg[binary] python-dotenv
```

## Configurar las variables de entorno

Copia `.env.example` a `.env` y completa los datos de tu conexión a PostgreSQL:

```sh
cp .env.example .env
```

Variables disponibles en `.env`:

| Variable       | Descripción                                   | Valor por defecto        |
|----------------|------------------------------------------------|---------------------------|
| `DB_DIALECT`   | Dialecto/driver de SQLAlchemy                  | `postgresql+psycopg`      |
| `DB_USER`      | Usuario de la base de datos                    | —                          |
| `DB_PASSWORD`  | Contraseña del usuario                         | —                          |
| `DB_HOST`      | Host de la base de datos                       | `localhost`                |
| `DB_PORT`      | Puerto de la base de datos                     | `5432`                      |
| `DB_NAME`      | Nombre de la base de datos                     | —                          |

El archivo `.env` está incluido en `.gitignore`, por lo que nunca se sube al repositorio.

## Crear la base de datos

Las tablas se crean automáticamente al ejecutar la aplicación (mediante `db.create_all()`). Si prefieres crearlas manualmente, puedes usar el script `db/tablas.sql` como referencia.

## Ejecutar la aplicación

Desde la carpeta `src`:

```sh
cd src
python3 app.py
```

Luego abre http://127.0.0.1:5000 en el navegador.

Para salir del entorno virtual:

```sh
deactivate
```

## Endpoints disponibles

| Método | Ruta                     | Descripción                                  |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/`                      | Ruta de prueba                                |
| POST   | `/register`              | Registra un nuevo usuario                     |
| POST   | `/login`                 | Inicia sesión con correo y contraseña         |
| GET    | `/notas`                 | Lista todas las notas                         |
| GET/POST | `/create-nota`         | Crea una nueva nota                           |
| GET    | `/notas/<id>`            | Consulta una nota específica                  |
| PUT    | `/notas/<id>`            | Actualiza una nota específica                 |
| DELETE | `/notas/<id>`            | Elimina una nota específica                   |
| GET/POST | `/create-article`      | Formulario y creación de un artículo (demo)    |
| GET    | `/article/<id>`         | Consulta un artículo específico (demo)         |

