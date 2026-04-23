import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint 1: Healthcheck (Requisito mínimo) 
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "El servicio está funcionando"}), 200

# Endpoint 2: Obtener usuarios (Ejemplo de ABM) [cite: 57]
@app.route('/users', methods=['GET'])
def get_users():
    # A futuro acá podés sumar la lógica de conexión a Postgres
    usuarios_mock = [{"id": 1, "nombre": "IAS Empleado"}]
    return jsonify({"users": usuarios_mock}), 200

# Endpoint 3: Crear un usuario (Completa los 3 endpoints mínimos) 
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    return jsonify({"message": "Usuario creado con éxito", "data": data}), 201

if __name__ == '__main__':
    # Uso de variable de entorno para evitar el debug=True hardcodeado 
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    
    # Se levanta el servidor
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)