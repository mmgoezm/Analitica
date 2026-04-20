import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. Simulación: Ciclo térmico de un horno (Estacionalidad Diaria)
tiempo = pd.date_range(start='2026-04-01', periods=168, freq='H') # 1 semana
# Ciclo senoidal de 24h + Ruido
estacionalidad = 10 * np.sin(2 * np.pi * np.arange(168) / 24)
temperatura = 180 + estacionalidad + np.random.normal(0, 1, 168)

df_temp = pd.DataFrame({'Temp_C': temperatura}, index=tiempo)

# 2. Descomposición de la Serie de Tiempo
# Aplicamos modelo aditivo: Yt = Tt + St + It
analisis = seasonal_decompose(df_temp['Temp_C'], model='additive', period=24)

# 3. Visualización de Componentes
plt.rcParams.update({'figure.figsize': (10,8)})
analisis.plot()
plt.suptitle('Descomposición de Componentes: Temperatura de Horno Industrial', fontsize=14)
plt.show()