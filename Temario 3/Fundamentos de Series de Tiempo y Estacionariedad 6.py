import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. DESCARGA DE DATOS
print("Descargando datos históricos de Yahoo Finance...")
ticker = "COP=X"
# Descargamos un periodo amplio para ver tendencias
df_divisa = yf.download(ticker, start="2016-01-01", end="2026-04-06")

# Limpieza: Aseguramos que trabajamos con una copia limpia de los precios de cierre
df_divisa = df_divisa[['Close']].copy()
df_divisa.columns = ['Precio_Cierre']

# 2. ANÁLISIS ESTADÍSTICO
print("\n--- RESUMEN ESTADÍSTICO DEL DÓLAR (USD/COP) ---")
# .describe() nos da la media, desviación y cuartiles del precio
print(df_divisa.describe().T)

# 3. CÁLCULO DE INDICADORES TEMPORALES
# Media móvil de 7 días y 30 días para suavizar la señal
df_divisa['MA_7'] = df_divisa['Precio_Cierre'].rolling(window=7).mean()
df_divisa['MA_30'] = df_divisa['Precio_Cierre'].rolling(window=30).mean()
df_divisa['MA_365'] = df_divisa['Precio_Cierre'].rolling(window=365).mean()

# 4. VISUALIZACIÓN TÉCNICA
plt.figure(figsize=(12, 6))
plt.plot(df_divisa['Precio_Cierre'], label='Precio Diario', color='lightgray', alpha=0.6)
plt.plot(df_divisa['MA_7'], label='Tendencia Semanal (MA 7)', color='orange')
plt.plot(df_divisa['MA_30'], label='Tendencia Mensual (MA 30)', color='blue', linewidth=2)
plt.plot(df_divisa['MA_365'], label='Tendencia Anual (MA 365)', color='green', linewidth=3)
plt.title('Análisis de Series de Tiempo: USD/COP', fontsize=14)
plt.ylabel('Pesos Colombianos ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

resultado_mult = seasonal_decompose(df_divisa['Precio_Cierre'], model='multiplicative', period=12)

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
resultado_mult.observed.plot(ax=axes[0], color='darkred', title='1. Señal Observada (Vibración con Amplitud Creciente)')
resultado_mult.trend.plot(ax=axes[1], color='blue', title='2. Tendencia (Desgaste Exponencial)')
resultado_mult.seasonal.plot(ax=axes[2], color='green', title='3. Estacionalidad (Proporcional a la Tendencia)')
resultado_mult.resid.plot(ax=axes[3], color='gray', linestyle='', marker='x', title='4. Residuos (Variación Relativa)')

plt.tight_layout()
plt.show()