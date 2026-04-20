import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. GENERACIÓN DE DATOS: Sensor de Temperatura (Modelo Aditivo)
# Simulación de 240 horas (10 días) de un horno con ciclo diario
np.random.seed(42)
tiempo = pd.date_range(start='2026-05-01', periods=240, freq='H')

# Componentes:
# Tendencia: El horno sube gradualmente de temperatura base
tendencia = np.linspace(150, 160, 240)
# Estacionalidad: Ciclo diario de +-5 grados (amplitud constante)
estacionalidad = 5 * np.sin(2 * np.pi * np.arange(240) / 24)
# Ruido: Variaciones aleatorias pequeñas
ruido = np.random.normal(0, 1, 240)

# Composición ADITIVA: Yt = Tt + St + It
y_aditiva = tendencia + estacionalidad + ruido
df_temp = pd.DataFrame({'Temperatura_C': y_aditiva}, index=tiempo)

# 2. DESCOMPOSICIÓN ADITIVA
# El periodo es 24 porque el ciclo se repite cada 24 horas
resultado_aditivo = seasonal_decompose(df_temp['Temperatura_C'], model='additive', period=24)

# 3. VISUALIZACIÓN DETALLADA
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
resultado_aditivo.observed.plot(ax=axes[0], color='black', title='1. Señal Observada (Original)')
resultado_aditivo.trend.plot(ax=axes[1], color='blue', title='2. Tendencia (Movimiento de largo plazo)')
resultado_aditivo.seasonal.plot(ax=axes[2], color='green', title='3. Estacionalidad (Patrón cíclico constante)')
resultado_aditivo.resid.plot(ax=axes[3], color='red', linestyle='', marker='o', title='4. Residuos (Ruido/Irregularidad)')

plt.tight_layout()
plt.show()