import pandas as pd
import requests
import matplotlib.pyplot as plt
import os

# 1. Configuración de Metadatos y API
CHANNEL_ID = "3256718"
READ_KEY = "D2RD28SPVIRB2N0R"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_KEY}&results=100"

try:
    # 2. Ingesta de datos (Pipeline)
    print("Descargando datos desde ThingSpeak...")
    response = requests.get(URL).json()
    df_nuevo = pd.DataFrame(response['feeds'])

    # 3. Transformación y Taxonomía de Datos
    # Convertimos strings a tipos numéricos y temporales para análisis
    df_nuevo['caudal_l_min'] = pd.to_numeric(df_nuevo['field1'])
    df_nuevo['temp_ambiente_c'] = pd.to_numeric(df_nuevo['field2'])
    df_nuevo['timestamp'] = pd.to_datetime(df_nuevo['created_at'])

    # Seleccionamos solo las columnas de interés para nuestra base de datos
    df_final = df_nuevo[['timestamp', 'caudal_l_min', 'temp_ambiente_c']]

    # 4. Almacenamiento en Archivo CSV (Base de Datos Local)
    archivo_csv = "base_datos_bombeo.csv"

    if not os.path.isfile(archivo_csv):
        # Si el archivo no existe, lo creamos con encabezados
        df_final.to_csv(archivo_csv, index=False)
        print(f"Base de datos creada: {archivo_csv}")
    else:
        # Si ya existe, añadimos los nuevos datos sin duplicar encabezados
        df_final.to_csv(archivo_csv, mode='a', header=False, index=False)
        print(f"Datos añadidos exitosamente a {archivo_csv}")

    # 5. Visualización de Tendencias (Imagen Emergente) 
    plt.figure(figsize=(12, 6))
    plt.plot(df_final['timestamp'], df_final['caudal_l_min'], label='Caudal (L/min)', color='blue')
    plt.plot(df_final['timestamp'], df_final['temp_ambiente_c'], label='Temp (°C)', color='red', alpha=0.5)

    plt.title("Analítica de Datos: Histórico de Sistema de Bombeo")
    plt.xlabel("Metadato: Tiempo de Captura")
    plt.ylabel("Valor Cuantitativo")
    plt.legend()
    plt.grid(True, linestyle='--')

    print("Generando visualización...")
    plt.show()

except Exception as e:
    print(f"Error en el flujo de datos: {e}")