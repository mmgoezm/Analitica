import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Simulación de Datos: Vibración en una bomba industrial
# Se genera una tendencia creciente (desgaste) + Ruido blanco
np.random.seed(2026)
tiempo = pd.date_range(start='2026-01-01', periods=200, freq='H')
tendencia_desgaste = np.linspace(0.5, 2.5, 200) # La vibración sube con el tiempo
ruido = np.random.normal(0, 0.2, 200)
vibracion = tendencia_desgaste + ruido

df_vibration = pd.DataFrame({'Vibracion_G': vibracion}, index=tiempo)

# 2. Análisis de Estacionariedad Visual
plt.figure(figsize=(10, 5))
plt.plot(df_vibration['Vibracion_G'], color='tab:red', label='Vibración Cruda')
plt.axhline(df_vibration['Vibracion_G'].mean(), color='black', linestyle='--', label='Media Global')

# 3. Cálculo de media móvil para resaltar la tendencia
df_vibration['Tendencia_MA'] = df_vibration['Vibracion_G'].rolling(window=24).mean()
plt.plot(df_vibration['Tendencia_MA'], color='blue', linewidth=2, label='Tendencia (Media Móvil 24h)')

plt.title('Monitoreo de Vibración: Identificación de No Estacionariedad')
plt.ylabel('Aceleración (Grms)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

