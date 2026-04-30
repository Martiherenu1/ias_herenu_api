import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("Falta configurar la variable de entorno DATABASE_URL")
    
    # RealDictCursor permite que Postgres nos devuelva diccionarios en lugar de tuplas,
    # lo cual es ideal para luego convertir a JSON.
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

# Inicialización: Creamos la tabla si no existe
def init_db():
    try:
        # Solo intentamos crear la tabla si la variable está configurada
        if os.environ.get('DATABASE_URL'):
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                );
            ''')
            conn.commit()
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Error al inicializar la DB: {e}")

# Ejecutamos la inicialización al arrancar la app
init_db()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Endpoint 1: Healthcheck (Requisito mínimo)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "El servicio está funcionando y listo"}), 200


# Endpoint 2: Obtener usuarios desde Postgres
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios;')
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"users": usuarios}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint 3: Crear un usuario en Postgres
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'nombre' not in data or 'email' not in data:
        return jsonify({"error": "Faltan datos obligatorios (nombre, email)"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id, nombre, email;',
            (data['nombre'], data['email'])
        )
        nuevo_usuario = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        print("Usuario creado con éxito", nuevo_usuario['nombre'], nuevo_usuario['email']  )
        return jsonify({"message": "Usuario creado con éxito", "data": nuevo_usuario}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "El email ya está registrado"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Uso de variable de entorno para evitar el debug=True hardcodeado
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)