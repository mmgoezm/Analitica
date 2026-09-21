import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración inicial
fecha_inicio = datetime(2024, 5, 1, 8, 0)
intervalo = 20 # minutos
total_puntos = (3 * 24 * 60) // intervalo # 3 días de datos
tiempos = [fecha_inicio + timedelta(minutes=i*intervalo) for i in range(total_puntos)]

# Generación de datos base (Comportamiento normal)
np.random.seed(42)
temp = np.random.normal(45, 1.5, total_puntos)    # 45°C promedio
presion = np.random.normal(101.5, 0.5, total_puntos) # 101.5 psi promedio
flujo = (presion * 0.5) + np.random.normal(10, 0.2, total_puntos) # Alta correlación [cite: 21]

df_bomba = pd.DataFrame({'Timestamp': tiempos, 'Temperatura': temp, 'Presion': presion, 'Flujo': flujo})

# --- EVENTO 1: Comportamiento atípico previo al mantenimiento (Día 2) ---
# Fluctuaciones constantes por 2 horas (6 puntos)
inicio_atipico = 80 # Punto arbitrario en el día 2
df_bomba.loc[inicio_atipico:inicio_atipico+6, ['Presion', 'Flujo']] += np.random.uniform(5, 15, (7, 2))

# --- EVENTO 2: Falla de mantenimiento (Sensores desconectados) ---
# 5 horas desconectados (15 puntos) inmediatamente después de la falla
inicio_falla = inicio_atipico + 7
df_bomba.loc[inicio_falla:inicio_falla+15, ['Presion', 'Flujo']] = np.nan

# --- EVENTO 3: Pérdidas por red (Día 3) ---
# Menor al 5% de pérdida aleatoria en el último tercio de los datos
puntos_dia3 = range(144, total_puntos)
indices_perdida = np.random.choice(puntos_dia3, size=int(len(puntos_dia3)*0.04), replace=False)
df_bomba.loc[indices_perdida, 'Temperatura'] = np.nan

# Guardar archivo
df_bomba.to_csv('datos_bomba_industrial.csv', index=False)
print("Archivo 'datos_bomba_industrial.csv' generado con éxito.")