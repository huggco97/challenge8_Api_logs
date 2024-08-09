from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Crear la base de datos y la tabla para almacenar logs
def init_db():
    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                nombre_servicio TEXT,
                nivel_log TEXT,
                mensaje TEXT,
                received_at TEXT
            )
        ''')
        

# Verificar el token de autenticación
def verify_token(token):
    valid_tokens = ["Bearer123"]  # Tokens válidos
    return token in valid_tokens

# Endpoint para recibir logs
@app.route('/logs', methods=['POST'])
def receive_log():
    print("Recibida solicitud POST en /logs")  # Añadir esta línea
    token = request.headers.get('Authorization')
    if not verify_token(token):
        print("Token no válido")  # Añadir esta línea
        return jsonify({"error": "Unauthorized"}), 401

    log_data = request.get_json()
    print(f"Datos de log recibidos: {log_data}")  # Añadir esta línea
    log_data['received_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect('logs.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (timestamp, nombre_servicio, nivel_log, mensaje, received_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (log_data['timestamp'], log_data['nombre_servicio'], log_data['nivel_log'], log_data['mensaje'], log_data['received_at']))
        print("Log insertado en la base de datos")  # Añadir esta línea
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")  # Añadir esta línea
        return jsonify({"error": "Database error"}), 500

    return jsonify({"status": "Log received"}), 200

# Endpoint para consultar logs con filtros
@app.route('/logs', methods=['GET'])
def get_logs():
    service_name = request.args.get('nombre_servicio')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if service_name:
        query += " AND nombre_servicio = ?"
        params.append(service_name)
    if start_date and end_date:
        query += " AND timestamp BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)

    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()

    return jsonify(logs), 200

if __name__ == '__main__':
    init_db()  # Crear la base de datos y tabla si no existen
    app.run(host='localhost', port=5000, debug= True)
