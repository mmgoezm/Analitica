import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Simulación: Voltaje (Estable) vs Corriente (Varianza Cambiante)
tiempo = np.arange(300)
voltaje = np.random.normal(120, 0.5, 300) # Varianza constante (Estacionario)

# Corriente con aumento de ruido en el centro
corriente_base = np.random.normal(5, 0.2, 300)
corriente_base[100:200] = np.random.normal(5, 1.5, 100) # Aumento drástico de varianza

df_power = pd.DataFrame({'Voltaje_V': voltaje, 'Corriente_A': corriente_base})

# 2. Análisis de Dispersión Temporal
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(df_power['Voltaje_V'], color='blue')
ax1.set_title('Voltaje: Estacionario (Media y Varianza Constantes)')
ax1.set_ylabel('Voltios (V)')

ax2.plot(df_power['Corriente_A'], color='orange')
ax2.set_title('Corriente: NO Estacionario (Varianza Cambiante / Ruido Variable)')
ax2.set_ylabel('Amperios (A)')

plt.xlabel('Muestras (Tiempo)')
plt.tight_layout()
plt.show()

# 3. Validación con Ventana Rodante (Rolling Standard Deviation)
plt.figure(figsize=(10, 4))
df_power['Corriente_A'].rolling(window=20).std().plot(label='Desviación Estándar Móvil (Corriente)')
plt.title('Detección de Heterocedasticidad (Cambio en Varianza)')
plt.legend()
plt.show()