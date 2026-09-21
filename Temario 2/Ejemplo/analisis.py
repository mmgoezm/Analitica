import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

# =================================================================
# 1. GENERACIÓN DEL DATASET (Simulación de Bomba Industrial) [cite: 12]
# =================================================================
np.random.seed(42)
fecha_inicio = datetime(2024, 5, 1, 8, 0)
intervalo = 20  # minutos
total_puntos = (3 * 24 * 60) // intervalo  # 3 días de datos
tiempos = [fecha_inicio + timedelta(minutes=i * intervalo) for i in range(total_puntos)]

# Comportamiento normal (Estado estacionario) [cite: 14, 15]
temp = np.random.normal(45, 1.5, total_puntos)
presion = np.random.normal(101.5, 0.5, total_puntos)
flujo = (presion * 0.5) + np.random.normal(10, 0.2, total_puntos)

df = pd.DataFrame({'Timestamp': tiempos, 'Temperatura': temp, 'Presion': presion, 'Flujo': flujo})

# --- EVENTO 1: Inestabilidad previa al mantenimiento (2 horas) [cite: 11, 20] ---
inicio_atipico = 80
indices_atipico = list(range(inicio_atipico, inicio_atipico + 7))
df.loc[indices_atipico, ['Presion', 'Flujo']] += np.random.uniform(5, 15, (7, 2))

# --- EVENTO 2: Desconexión de sensores (Mantenimiento - 5 horas) [cite: 30] ---
inicio_falla = inicio_atipico + 7
indices_falla = list(range(inicio_falla, inicio_falla + 16))
df.loc[indices_falla, ['Presion', 'Flujo']] = np.nan

# --- EVENTO 3: Pérdidas de red en Día 3 (< 5%) [cite: 30] ---
indices_dia3 = range(144, total_puntos)
indices_perdida = np.random.choice(indices_dia3, size=int(len(indices_dia3) * 0.04), replace=False)
df.loc[indices_perdida, 'Temperatura'] = np.nan

# =================================================================
# 2. ANÁLISIS EXPLORATORIO (EDA) Y FILTRADO
# =================================================================
# Filtrado de datos para análisis específicos
df_sin_desconexion = df.drop(indices_falla)  # Para Boxplots (incluye atípicos) [cite: 11, 19]
df_tipico = df_sin_desconexion.drop(indices_atipico, errors='ignore').dropna()  # Estado Estacionario Real


def calcular_iqr_limites(columna):
    q1 = columna.quantile(0.25)
    q3 = columna.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


# =================================================================
# 3. PREPROCESAMIENTO (IMPUTACIÓN Y ESCALADO) [cite: 22, 30]
# =================================================================
# Imputación Estadística (Mediana para fallas críticas) [cite: 30]
df['Presion_Imp'] = df['Presion'].fillna(df['Presion'].median())
df['Flujo_Imp'] = df['Flujo'].fillna(df['Flujo'].median())

# Imputación por Interpolación (Pérdidas de red leves) [cite: 30]
df['Temp_Imp'] = df['Temperatura'].interpolate(method='linear')

# Escalado de Datos (StandardScaler: Media 0, Desviación 1) [cite: 32, 34]
scaler = StandardScaler()
df_std = pd.DataFrame(scaler.fit_transform(df[['Temp_Imp', 'Presion_Imp', 'Flujo_Imp']]),
                      columns=['Temp_Std', 'Presion_Std', 'Flujo_Std'])

# =================================================================
# 4. VISUALIZACIÓN INTEGRADA [cite: 11, 18, 19]
# =================================================================

# --- GRÁFICA 1: Series de Tiempo Originales ---
fig1, axes1 = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
variables = ['Temperatura', 'Presion', 'Flujo']
colores = ['#3498db', '#2ecc71', '#e67e22']

for i, var in enumerate(variables):
    sns.lineplot(data=df, x='Timestamp', y=var, ax=axes1[i], color=colores[i])
    axes1[i].set_title(f'Serie de Tiempo Original: {var}')
plt.tight_layout()
plt.show()

# --- GRÁFICA 2: EDA (Boxplots e Histogramas) [cite: 18, 19] ---
fig2, axes2 = plt.subplots(2, 3, figsize=(18, 10))
for i, var in enumerate(variables):
    # Fila 1: Boxplots sin desconexión [cite: 19]
    sns.boxplot(x=df_sin_desconexion[var], ax=axes2[0, i], color=colores[i])
    axes2[0, i].set_title(f'Boxplot: {var}\n(Detección de Atípicos)')
    inf, sup = calcular_iqr_limites(df_sin_desconexion[var])
    axes2[0, i].set_xlabel(f'Límites IQR: [{inf:.2f}, {sup:.2f}]')

    # Fila 2: Histogramas de Distribución Típica [cite: 18]
    sns.histplot(df_tipico[var], kde=True, ax=axes2[1, i], color=colores[i])
    axes2[1, i].set_title(f'Distribución Típica: {var}\n(Estado Estacionario)')
plt.tight_layout()
plt.show()

# --- GRÁFICA 3: Tabla de Estadísticas Típicas [cite: 14, 15, 16, 17] ---
stats = df_tipico[variables].agg(['mean', 'std', 'var', 'min', 'max']).T
stats.columns = ['Media', 'Desv. Estándar', 'Varianza', 'Mínimo', 'Máximo']
stats = stats.round(4)

fig3, ax3 = plt.subplots(figsize=(10, 3))
ax3.axis('off')
tabla = ax3.table(cellText=stats.values, rowLabels=stats.index, colLabels=stats.columns,
                  cellLoc='center', loc='center', colColours=["#f2f2f2"] * 5)
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.8)
plt.title('Métricas de Comportamiento Típico (Distribución Estacionaria)', pad=20)
plt.show()

# --- GRÁFICA 4: Zonas de Interés e Imputación [cite: 20, 30] ---
fig4, axes4 = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
# Presión: Falla y Mantenimiento
sns.lineplot(data=df, x='Timestamp', y='Presion_Imp', ax=axes4[0], color='gray', linestyle='--',
             label='Imputada (Mediana)')
sns.lineplot(data=df, x='Timestamp', y='Presion', ax=axes4[0], color='#2ecc71', label='Real')
axes4[0].axvspan(df['Timestamp'].iloc[indices_atipico[0]], df['Timestamp'].iloc[indices_falla[-1]],
                 color='red', alpha=0.2, label='Zona de Interés (Inestabilidad y Falla)')
axes4[0].set_title('Análisis de Zonas Críticas: Presión')
axes4[0].legend()

# Temperatura: Pérdidas de red
sns.lineplot(data=df, x='Timestamp', y='Temp_Imp', ax=axes4[1], color='gray', linestyle='--',
             label='Imputada (Interpolación)')
sns.lineplot(data=df, x='Timestamp', y='Temperatura', ax=axes4[1], color='#3498db', label='Real')
axes4[1].set_title('Análisis de Zonas Críticas: Temperatura (Pérdidas de Red)')
axes4[1].legend()
plt.tight_layout()
plt.show()

# --- GRÁFICA 5: Matriz de Correlación [cite: 21] ---
plt.figure(figsize=(8, 5))
sns.heatmap(df_tipico[variables].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación en Estado Estacionario')
plt.show()

print("--- ANALISIS FINALIZADO ---")
print(stats)