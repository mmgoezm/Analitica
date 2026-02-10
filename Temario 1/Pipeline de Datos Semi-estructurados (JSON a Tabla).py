import pandas as pd
import json

# Simulación de datos provenientes de diferentes tipos de almacenamiento [cite: 23]
json_data = """
[
    {"id": 1, "tipo": "Caudal", "valor": "120.5", "unidad": "m3/h", "status": "OK"},
    {"id": 2, "tipo": "Caudal", "valor": "118.2", "unidad": "m3/h", "status": "OK"},
    {"id": 3, "tipo": "Caudal", "valor": "22.5", "unidad": "m3/h", "status": "OK"},
    {"id": 4, "tipo": "Caudal", "valor": "22.9", "unidad": "m3/h", "status": "OK"},
    {"id": 5, "tipo": "Caudal", "valor": "222.5", "unidad": "m3/h", "status": "OK"},
    {"id": 6, "tipo": "Caudal", "valor": "error", "unidad": "m3/h", "status": "FAIL"}
]
"""



def pipeline_limpieza(datos_json):
    # 1. Ingesta
    df = pd.DataFrame(json.loads(datos_json))

    # 2. Transformación de tipos (De String a Numérico)
    # Convertimos 'valor' a float, los errores se vuelven NaN (Not a Number)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    # 3. Tratamiento de datos faltantes (Importante en analítica de ingeniería)
    df = df.dropna(subset=['valor'])

    return df


tabla_ingenieria = pipeline_limpieza(json_data)
print("Datos procesados listos para análisis:")
print(tabla_ingenieria.info())  # Muestra la taxonomía técnica de la tabla
print(tabla_ingenieria)