import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 1. Creación del Dataset (Simulación de sensores industriales)
# El 'flujo' se diseña para tener alta correlación con la 'presion'
np.random.seed(42)

#Datos 1
presion_base = np.array([101.2, 101.5, 101.1, 101.8, 102.0, 101.4, 101.6, 101.2, 101.5, 101.3])

data = {
    'temperatura': [22.1, 23.4, 22.8, 23.1, 22.5, 23.9, 28.0, 22.2, 23.5, np.nan],
    'presion': presion_base,
    'flujo': (presion_base * 2.5) - 200 + np.random.normal(0, 0.1, 10)  # Alta correlación con presión
}
# Introducimos un valor nulo en flujo para mostrar imputación
data['flujo'][4] = np.nan

# Datos  2"

data2 = {
    'temperatura':np.random.normal(loc=2, scale=30, size=(30)),
    'presion': np.random.normal(loc=50, scale=15, size=(30)),
    'flujo': np.random.normal(loc=25, scale=30, size=(30))
}


df = pd.DataFrame(data2)
print(df)

# 2. Análisis Exploratorio de Datos (EDA)
def calcular_estadisticas_iqr(df, columna):
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return Q1, Q3, IQR, limite_inferior, limite_superior


print("--- Estadísticas Descriptivas y Atípicos ---")
for col in df.columns:
    q1, q3, iqr, l_inf, l_sup = calcular_estadisticas_iqr(df, col)
    # Medidas de tendencia central y dispersión
    print(f"Variable: {col.capitalize()}")
    print(f"Media: {df[col].mean():.2f} | Mediana: {df[col].median():.2f}")
    print(f"Límites IQR: [{l_inf:.2f}, {l_sup:.2f}]")

    # Detección de atípicos (Outliers)
    outliers = df[(df[col] < l_inf) | (df[col] > l_sup)][col].values
    print(f"Atípicos: {outliers}\n")

# Visualización
fig, axes = plt.subplots(3, 2, figsize=(12, 15))
colores = ['skyblue', 'lightgreen', 'orange']

for i, col in enumerate(df.columns):
    sns.histplot(df[col].dropna(), kde=True, ax=axes[i, 0], color=colores[i])
    axes[i, 0].set_title(f'Distribución de {col.capitalize()}')

    sns.boxplot(x=df[col], ax=axes[i, 1], color=colores[i])
    axes[i, 1].set_title(f'Boxplot de {col.capitalize()}')


plt.tight_layout(pad=3.0)
plt.show()


# 3. Tratamiento de Datos Faltantes (Imputación)
print("--- Métodos de Imputación ---")
# Opción A: Imputación Estadística (Media o Mediana)
df['temp_media'] = df['temperatura'].fillna(df['temperatura'].mean())
df['temp_mediana'] = df['temperatura'].fillna(df['temperatura'].median())

# Opción B: Interpolación (Útil en series de tiempo o procesos continuos)
df['flujo_interpolado'] = df['flujo'].interpolate(method='linear')

print(f"Valores nulos originales en flujo: {df['flujo'].isnull().sum()}")
print(f"Valores nulos tras interpolación: {df['flujo_interpolado'].isnull().sum()}\n")

# 4. Escalado de Datos
# Trabajaremos con las versiones limpias
X = df[['temp_mediana', 'presion', 'flujo_interpolado']]

# Normalización (Min-Max): Rango [0, 1]
scaler_minmax=MinMaxScaler()
X_minmax = pd.DataFrame(scaler_minmax.fit_transform(X), columns=[f'{c}_MinMax' for c in X.columns])

# Estandarización (StandardScaler): Media 0, Desv. Est. 1
scaler_std = StandardScaler()
X_std = pd.DataFrame(scaler_std.fit_transform(X), columns=[f'{c}_Std' for c in X.columns])

print("Datos Estandarizados (Primeras filas):")
print(X_std.head())

# 5. Relación entre Variables (Correlación)
plt.figure(figsize=(8, 6))
matriz_corr = X.corr()
sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación: Temperatura, Presión y Flujo')
plt.show()