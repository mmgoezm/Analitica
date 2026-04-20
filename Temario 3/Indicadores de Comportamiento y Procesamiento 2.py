import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# 1. OBTENCIÓN DE DATOS (Medellín - Últimos 5 días)
url = "https://archive-api.open-meteo.com/v1/archive?latitude=6.25&longitude=-75.56&start_date=2026-04-01&end_date=2026-04-05&hourly=temperature_2m"
data = requests.get(url).json()

df = pd.DataFrame({
    'Fecha': pd.to_datetime(data['hourly']['time']),
    'Temp_C': data['hourly']['temperature_2m']
}).set_index('Fecha')

# 2. INDICADORES DE COMPORTAMIENTO (Ventana de 6 horas)
# Media Móvil: Suaviza la señal (Filtro pasa-bajo)
df['Media_Movil_6h'] = df['Temp_C'].rolling(window=6).mean()
# Desviación Estándar Móvil: Mide la estabilidad/ruido en el tiempo
df['Std_Movil_6h'] = df['Temp_C'].rolling(window=6).std()

# 3. VISUALIZACIÓN TÉCNICA
plt.figure(figsize=(14, 7))

# Subplot 1: Señal Suavizada
plt.subplot(2, 1, 1)
plt.plot(df.index, df['Temp_C'], label='Señal Cruda', color='lightgray', alpha=0.7)
plt.plot(df.index, df['Media_Movil_6h'], label='Media Móvil (6h)', color='blue', linewidth=2)
plt.title('Suavizado de Señal Térmica en Medellín', fontsize=14)
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(alpha=0.3)

# Subplot 2: Análisis de Estabilidad (Varianza)
plt.subplot(2, 1, 2)
plt.fill_between(df.index, df['Std_Movil_6h'], color='orange', alpha=0.3, label='Inestabilidad (Std Dev)')
plt.title('Variabilidad de la Señal en Ventanas de 6 Horas', fontsize=12)
plt.ylabel('Desviación (°C)')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Resumen estadístico de los nuevos indicadores
print("\n--- ANÁLISIS DE INDICADORES DE PROCESAMIENTO ---")
print(df[['Temp_C', 'Media_Movil_6h', 'Std_Movil_6h']].describe().T)