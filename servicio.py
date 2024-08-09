import time
import requests
import json
import random
from datetime import datetime

# Configuración básica del servicio
SERVICE_NAME = "Servicio1"
LOG_LEVELS = ["INFO", "ERROR", "DEBUG", "WARNING"]

# URL del servidor central de logging (para probar, puedes usar localhost)
SERVER_URL = "http://localhost:5000/logs"

# Función para generar un log
def generar_log():
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre_servicio": SERVICE_NAME,
        "nivel_log": random.choice(LOG_LEVELS),  # Por simplicidad, todos los logs serán "INFO"
        "mensaje":  f'Este es un registro (log) de {SERVICE_NAME}'
    }
    return log

# Función para enviar el log al servidor central
def send_log(log):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer123"  # Aquí iría tu token de autenticación
    }
    response = requests.post(SERVER_URL, headers=headers, data=json.dumps(log))
    if response.status_code == 200:
        print("Log enviado correctamente.")
    else:
        print(f"Error al enviar el log: {response.status_code}, {response.text}")

# Simulando la generación y envío de logs cada 5 segundos
if __name__ == "__main__":
    while True:
        log = generar_log()
        send_log(log)
        time.sleep(5)
