import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 1. CREACIÓN DEL DATAFRAME
datos_sensores = {
    'ID_Nodo': [1, 2, 3, 4, 5, 6],                              # Metadatos [cite: 41]
    'Voltaje_V': [218.5, 220.1, 219.8, 221.0, 190.2, 220.5],    # Variable cuantitativa [cite: 37]
    'Corriente_A': [5.2, 5.1, 4.9, 5.0, 12.5, 5.1],             # Notar el outlier en el Nodo 5
    'Estado': ['Normal', 'Normal', 'Normal', 'Normal', 'Alerta', 'Normal'] # Cualitativa [cite: 37]
}

# Convertimos el diccionario en un DataFrame
df = pd.DataFrame(datos_sensores)

print("--- VISTA DEL DATAFRAME INDUSTRIAL ---")
print(df)

# 2. EL MÉTODO .DESCRIBE()
# Este método genera un resumen automático de las variables numéricas
resumen = df.describe()

print("\n--- RESUMEN ESTADÍSTICO (.describe) ---")
print(resumen)

