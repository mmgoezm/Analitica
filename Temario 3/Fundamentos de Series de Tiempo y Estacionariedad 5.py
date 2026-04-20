import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. GENERACIÓN DE DATOS: Sensor de Vibración (Modelo Multiplicativo)
# Simulación de 240 muestras de una bomba con desgaste progresivo
np.random.seed(2026)
tiempo = pd.date_range(start='2026-06-01', periods=240, freq='H')

# Componentes:
# Tendencia: Crecimiento exponencial del desgaste
tendencia = np.linspace(1, 10, 240)
# Estacionalidad: El patrón se amplifica a medida que la tendencia sube
# Notar que aquí la amplitud es relativa (multiplicativa)
estacionalidad = 1 + 0.5 * np.sin(2 * np.pi * np.arange(240) / 12) # Ciclo cada 12h
# Ruido: También se amplifica con la tendencia
ruido = 1 + np.random.normal(0, 0.05, 240)

# Composición MULTIPLICATIVA: Yt = Tt * St * It
y_multiplicativa = tendencia * estacionalidad * ruido
df_vibration = pd.DataFrame({'Vibracion_G': y_multiplicativa}, index=tiempo)

# 2. DESCOMPOSICIÓN MULTIPLICATIVA
resultado_mult = seasonal_decompose(df_vibration['Vibracion_G'], model='multiplicative', period=12)

# 3. VISUALIZACIÓN DETALLADA
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
resultado_mult.observed.plot(ax=axes[0], color='darkred', title='1. Señal Observada (Vibración con Amplitud Creciente)')
resultado_mult.trend.plot(ax=axes[1], color='blue', title='2. Tendencia (Desgaste Exponencial)')
resultado_mult.seasonal.plot(ax=axes[2], color='green', title='3. Estacionalidad (Proporcional a la Tendencia)')
resultado_mult.resid.plot(ax=axes[3], color='gray', linestyle='', marker='x', title='4. Residuos (Variación Relativa)')

plt.tight_layout()
plt.show()