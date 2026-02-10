import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# 1. GENERACIÓN DE DATOS
def simular_sistema_completo(n=150):
    inicio = datetime.now()
    tiempos = [inicio + timedelta(minutes=10 * i) for i in range(n)]

    # Variables Cuantitativas Continuas
    presion = 55 + np.random.normal(0, 1.5, n)
    caudal = 120 + np.random.normal(0, 3, n)
    temperatura = 40 + np.random.normal(0, 0.5, n)
    vibracion = 0.05 + np.random.normal(0, 0.01, n)
    potencia = 15 + np.random.normal(0, 0.2, n)

    # SIMULACIÓN DE FALLO: Del punto 100 al 130 el sistema falla
    presion[100:130] *= 0.6  # Cae la presión
    caudal[100:130] *= 0.5  # Cae el caudal
    temperatura[110:140] += 15  # La temperatura sube por esfuerzo
    vibracion[100:130] *= 3  # El equipo vibra por la inestabilidad

    return pd.DataFrame({
        'tiempo': tiempos,
        'presion_psi': presion,
        'caudal_m3h': caudal,
        'temp_c': temperatura,
        'vibracion_mm_s': vibracion,
        'potencia_kw': potencia
    })


# 2. ANALÍTICA DE DATOS
def realizar_analitica(df):
    # Calculamos un KPI compuesto (Eficiencia Hidráulica)
    df['eficiencia'] = (df['presion_psi'] * df['caudal_m3h']) / df['potencia_kw']

    # Creamos variables Cualitativas/Booleanas para las alertas
    umbral_efi = df['eficiencia'].mean() - 1.2 * df['eficiencia'].std()
    df['alerta'] = (df['eficiencia'] < umbral_efi) | (df['temp_c'] > 50)

    return df


# Ejecución
df_final = realizar_analitica(simular_sistema_completo(150))

# 3. VISUALIZACIÓN
fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# Panel 1: Hidráulica
axes[0].plot(df_final['tiempo'], df_final['presion_psi'], label='Presión (PSI)', color='blue')
axes[0].plot(df_final['tiempo'], df_final['caudal_m3h'], label='Caudal (m³/h)', color='cyan')
axes[0].set_title('Variables Hidráulicas (Cuantitativas)')
axes[0].legend()

# Panel 2: Mecánica (Doble eje Y)
axes[1].plot(df_final['tiempo'], df_final['temp_c'], label='Temp (°C)', color='red')
ax2 = axes[1].twinx()
ax2.plot(df_final['tiempo'], df_final['vibracion_mm_s'], label='Vibración (mm/s)', color='purple', linestyle='--')
axes[1].set_title('Variables de Estado Mecánico')
axes[1].legend(loc='upper left')
ax2.legend(loc='upper right')

# Panel 3: Diagnóstico Final
axes[2].plot(df_final['tiempo'], df_final['eficiencia'], label='Índice de Salud', color='green')
alertas = df_final[df_final['alerta']]
axes[2].scatter(alertas['tiempo'], alertas['eficiencia'], color='darkred', label='FALLO DETECTADO', zorder=5)
axes[2].set_title('Analítica Prescriptiva: Diagnóstico Automático')
axes[2].legend()

plt.tight_layout()
plt.show()