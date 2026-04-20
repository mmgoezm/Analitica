import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import warnings

# Ignorar avisos de visualización
warnings.filterwarnings("ignore")

# 1. OBTENCIÓN DE DATOS (Bitcoin - Últimos 30 días)
print("Descargando datos de alta volatilidad (BTC-USD)...")
df_btc = yf.download("BTC-USD", period="30d", interval="1h")

if isinstance(df_btc.columns, pd.MultiIndex):
    df_btc.columns = df_btc.columns.get_level_values(0)

# 2. PROCESAMIENTO: Aseguramos que tenemos datos limpios
df_btc = df_btc[['Close']].copy()
df_btc = df_btc.dropna()

# 3. VISUALIZACIÓN COMPARATIVA
plt.style.use('ggplot')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# --- Gráfico Superior: Precio del Bitcoin ---
# Nota: Usamos 'orange' o 'gold' (sin 'tab:')
ax1.plot(df_btc.index, df_btc['Close'], color='orange', linewidth=2, label='Precio BTC (USD)')
ax1.set_title('Comportamiento del Bitcoin (BTC) - Ventana de 30 Días', fontsize=16, fontweight='bold')
ax1.set_ylabel('Precio en USD ($)')
ax1.legend()
ax1.grid(alpha=0.3)

# --- Gráfico Inferior: Autocorrelación (ACF) ---
# Aquí veremos la "Memoria Débil" del mercado
plot_acf(df_btc['Close'], lags=160, ax=ax2, color='darkred', vlines_kwargs={"colors": 'darkred'})
ax2.set_title('Gráfica de Autocorrelación (ACF) - "Memoria Débil"', fontsize=14)
ax2.set_xlabel('Retardo en Horas (Lags)')
ax2.set_ylabel('Coeficiente de Correlación')
ax2.set_ylim([-0.2, 1.1])
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# 4. DIAGNÓSTICO EN CONSOLA
print(f"\n--- ANÁLISIS DE MEMORIA (BTC) ---")
print(f"Inercia a 1 hora: {df_btc['Close'].autocorr(lag=1):.4f}")
print(f"Inercia a 24 horas: {df_btc['Close'].autocorr(lag=24):.4f}")