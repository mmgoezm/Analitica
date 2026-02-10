import requests
import time
import random

# 1. Configuración de Metadatos (Credenciales de ThingSpeak)
# Sustituye con tu 'Write API Key' de la pestaña API Keys en ThingSpeak
WRITE_API_KEY = "71USHPVXAH67IFE1"
URL_BASE = "https://api.thingspeak.com/update"


def simular_envio_datos(intervalo_segundos=60):
    """
    Genera datos aleatorios y los envía a ThingSpeak cada N segundos.
    """
    print(f"Iniciando simulación de envío a ThingSpeak cada {intervalo_segundos} segundos...")
    print("Presiona Ctrl+C para detener la simulación.\n")

    try:
        while True:
            # 2. Generación de Variables Cuantitativas (Simulación de Sensores)
            # Caudal en $L/min$ (Variable continua)
            caudal = round(random.uniform(15.0, 45.0), 2)

            # Temperatura en $^\circ C$ (Variable continua)
            temperatura = round(random.uniform(22.0, 28.0), 2)

            # 3. Empaquetado de Datos (Estructura de Envío)
            parametros = {
                "api_key": WRITE_API_KEY,
                "field1": caudal,
                "field2": temperatura
            }

            # 4. Envío de Información (Protocolo HTTP GET)
            respuesta = requests.get(URL_BASE, params=parametros)

            # 5. Verificación del Pipeline
            if respuesta.status_code == 200:
                # ThingSpeak responde con el número de la entrada (entry_id) si tiene éxito
                print(f"[{time.strftime('%H:%M:%S')}] Datos enviados con éxito.")
                print(f" > Caudal: {caudal} L/min | Temp: {temperatura} °C | ID Entrada: {respuesta.text}")
            else:
                print(f"Error al enviar datos. Código de estado: {respuesta.status_code}")

            # Espera para cumplir con el intervalo (Metadato Temporal)
            time.sleep(intervalo_segundos)

    except KeyboardInterrupt:
        print("\nSimulación finalizada por el usuario.")


# Ejecutar el simulador
if __name__ == "__main__":
    simular_envio_datos(60)  # Envío cada 1 minuto según tu requerimiento