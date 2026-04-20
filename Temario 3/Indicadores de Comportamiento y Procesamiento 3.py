import pandas as pd
import requests
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import seaborn as sns

# 1. OBTENCIÓN DE DATOS (Medellín - 20 Días: del 17 de Marzo al 5 de Abril, 2026)
url = "https://archive-api.open-meteo.com/v1/archive?latitude=6.25&longitude=-75.56&start_date=2026-03-17&end_date=2026-04-05&hourly=temperature_2m"
data = requests.get(url).json()

df_20d = pd.DataFrame({
    'Fecha': pd.to_datetime(data['hourly']['time']),
    'Temp_C': data['hourly']['temperature_2m']
}).set_index('Fecha')

# 2. PROCESAMIENTO DE INDICADORES
# Cambio porcentual para medir la estabilidad de los 20 días
df_20d['Volatilidad_%'] = df_20d['Temp_C'].pct_change() * 100

# 3. VISUALIZACIÓN INTEGRAL
fig = plt.figure(figsize=(15, 10))
grid = fig.add_gridspec(2, 1, height_ratios=[1, 1.2])

# --- Gráfico Superior: La serie de tiempo completa ---
ax1 = fig.add_subplot(grid[0])
ax1.plot(df_20d.index, df_20d['Temp_C'], color='tab:orange', linewidth=1.5, label='Temperatura Real')
ax1.set_title('Monitoreo Climático Medellín - Ventana de 20 Días', fontsize=16, fontweight='bold')
ax1.set_ylabel('Grados Celsius (°C)')
ax1.grid(alpha=0.3)
ax1.legend()

# --- Gráfico Inferior: Autocorrelación (ACF) ---
# Analizaremos los rezagos (lags) de las últimas 48 horas (2 días completos)
ax2 = fig.add_subplot(grid[1])
plot_acf(df_20d['Temp_C'], lags=48, ax=ax2, color='darkblue', vlines_kwargs={"colors": 'darkblue'})
ax2.set_title('Gráfica de Autocorrelación (ACF) - Memoria del Sistema', fontsize=14)
ax2.set_xlabel('Retardo en Horas (Lags)')
ax2.set_ylabel('Coeficiente de Correlación')
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()

# 4. INSIGHTS PARA LA CLASE
print(f"--- REPORTE DE MEMORIA TEMPORAL ---")
print(f"Correlación a 1 hora (Inercia inmediata): {df_20d['Temp_C'].autocorr(lag=1):.4f}")
print(f"Correlación a 24 horas (Ciclo diario): {df_20d['Temp_C'].autocorr(lag=24):.4f}")