import pandas as pd
import requests
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

# 1. ADQUISICIÓN DE DATOS (5 días de historia en Medellín)
# Coordenadas: Lat 6.25, Lon -75.56
url = "https://archive-api.open-meteo.com/v1/archive?latitude=6.25&longitude=-75.56&start_date=2026-04-01&end_date=2026-04-05&hourly=temperature_2m"

response = requests.get(url)
data = response.json()

df = pd.DataFrame({
    'Fecha': pd.to_datetime(data['hourly']['time']),
    'Temp': data['hourly']['temperature_2m']
}).set_index('Fecha')

# 2. ENTRENAMIENTO Y AJUSTE (Fitted Values)
# Modelo AR(24): Memoria de un día completo
modelo_ar = AutoReg(df['Temp'], lags=24).fit()
ajuste_ar = modelo_ar.fittedvalues # Valores del modelo sobre el pasado

# Modelo ARIMA(24, 1, 1): Estabilización por diferenciación
modelo_arima = ARIMA(df['Temp'], order=(24, 1, 10)).fit()
ajuste_arima = modelo_arima.fittedvalues

# 3. PREDICCIÓN DE UN DÍA COMPLETO (24 Horas)
pred_ar = modelo_ar.predict(start=len(df), end=len(df)+23)
pred_arima = modelo_arima.forecast(steps=24)

# 4. VISUALIZACIÓN INTEGRAL
plt.figure(figsize=(15, 7))

# Datos Históricos Reales
plt.plot(df.index, df['Temp'], label='Histórico Real', color='black', alpha=0.4, linewidth=3)

# Ajuste de los modelos sobre la historia (Ver qué tan bien aprendieron)
plt.plot(ajuste_ar.index, ajuste_ar, label='Ajuste Histórico AR', color='blue', linestyle=':', alpha=0.7)
plt.plot(ajuste_arima.index, ajuste_arima, label='Ajuste Histórico ARIMA', color='green', linestyle=':', alpha=0.7)

# Predicción del futuro (24 horas)
eje_futuro = pd.date_range(start=df.index[-1] + pd.Timedelta(hours=1), periods=24, freq='H')
plt.plot(eje_futuro, pred_ar, label='Predicción 24h (AR)', color='blue', linewidth=2)
plt.plot(eje_futuro, pred_arima, label='Predicción 24h (ARIMA)', color='green', linewidth=2)

# Estética de la gráfica
plt.axvline(df.index[-1], color='red', linestyle='--', label='Inicio de Predicción')
plt.title('Análisis y Predicción Climática: Medellín (ITM 2026)', fontsize=16)
plt.ylabel('Temperatura (°C)')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 5. CÁLCULO DE ERROR (Saber Procedimental)
error_ar = (df['Temp'][24:] - ajuste_ar).abs().mean()
print(f"Error Medio Absoluto (MAE) del Modelo AR: {error_ar:.2f}°C")