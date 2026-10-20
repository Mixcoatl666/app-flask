# Instrucciones del repositorio

## Reglas

1. No escribir código sin que se indique explicitamente.
2. Al escribir código respetar la jerarquía del proyecto y diseños que se encuentran disponibles.
3. Cuando escribas código, aprovecha las skills de `ponytail` y `clean-code`.

## Estructura y ejecución

- Es una API Flask monolítica; el punto de entrada es `src/app.py` y los modelos están en `src/models/`.
- El código importa `models` desde `src`; ejecuta la aplicación desde esa carpeta: `cd src && python3 app.py`.
- El servidor de desarrollo escucha en el puerto `5001`; el `5000` mencionado en `README.md` está desactualizado.
- No hay suite de tests, linter, typecheck ni migraciones configurados en el repositorio; no inventes comandos de verificación para ellos.

## Configuración y base de datos

- Usa PostgreSQL con el driver `postgresql+psycopg`. Configura `.env` a partir de `.env.example` y añade también `SECRET_KEY`, que la aplicación necesita para las sesiones aunque no aparece en el ejemplo.
- Preparación local: `python3 -m venv venv`, `source venv/bin/activate`, `python -m pip install Flask Flask-SQLAlchemy psycopg[binary] python-dotenv`.
- `db.create_all()` se ejecuta al cargar `src/app.py`; no hay herramienta de migraciones. `db/tablas.sql` es solo una referencia para usuarios, no el esquema completo.
- La autenticación usa la sesión de Flask y CORS está configurado con credenciales; los clientes frontend deben enviar las cookies/credenciales en sus peticiones.

## Convenciones y gotchas verificados

- Respeta los nombres actuales del modelo: `Notas.idusuario` (no `user_id`) y `Notas.create_at`; `Usuario` usa `idusuario` y `created_at`. No renombres columnas sin actualizar el esquema.
- El campo `Notas.is_favorite` está almacenado en la nota, por lo que actualmente el favorito es global a la nota, no independiente por usuario.
- No modifiques código de aplicación sin una petición explícita; conserva la jerarquía existente (`src/app.py` y `src/models/`).
