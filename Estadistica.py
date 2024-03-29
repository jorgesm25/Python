################################################################################
#          			Estadísticas de resumen                        # 
################################################################################

#---------------------Resumen estadístico------------------
resultados = df.groupby('Género').agg({
    'Articulos': ['count', 'mean', 'median', 'std', lambda x: x.quantile(0.75) - x.quantile(0.25)]
}).reset_index()

resultados.columns = ['Género', 'Recuento', 'Media', 'Mediana', 'DesvEstandar', 'RICuartil']

print(resultados)

#--------------------- Tabla cruzada------------------
tabla_cruzada = pd.crosstab(df['Género'], df['Grado'], margins=True, margins_name='Total')
print(tabla_cruzada)

#Tabla cruzada con estadísticas
import pingouin as pg
tabla_cruzada = pd.crosstab(df['Género'], df['Grado'])

resultado = pg.chi2_independence(df, x='Género', y='Grado')

print(tabla_cruzada)
print(resultado)

#--------------------- NORMALIDAD------------------
# Eliminar filas con valores faltantes en 'Citas'
df = df.dropna(subset=['Citas'])

# Prueba de Shapiro-Wilk
shapiro(df['Citas'])

#Grafico Q-Q
import statsmodels.api as sm
import matplotlib.pyplot as plt

citas = df['Citas']

# Crear el Q-Q plot
sm.qqplot(citas, line='s')
plt.show()

#------------- INTERVALO DE CONFIANZA CON BOOSTRAP-----------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Variable de interes "grado" caso de exito "doctorado"
prop_doctorado_poblacion = df['grado'].eq('Doctorado').mean()
print(f"Proporción de doctorados en la población completa: {prop_doctorado_poblacion}")

# Crear una lista para almacenar los resultados
resultados_list = []

# crear 500 conjuntos mediante remuestreo y obtener el estadistico muestral
sample_prop_doctorado = []
for i in range(500):
    # Realizar un remuestreo de los datos
    muestra = df.sample(frac=1, replace=True)
    # Calcular la proporción de doctorados en la muestra remuestreada
    prop_doctorado_muestra = muestra['grado'].eq('Doctorado').mean()
    sample_prop_doctorado.append(prop_doctorado_muestra)
    # Agregar los resultados a la lista
    resultados_list.append({'Número de muestra': i + 1, 'Proporción de doctorado': prop_doctorado_muestra})

# Convertir la lista de resultados en un DataFrame
resultados = pd.DataFrame(resultados_list)

# Imprimir la media de las proporciones de doctorados en las muestras
print(f"Media de las proporciones de doctorados en las muestras: {np.mean(sample_prop_doctorado)}")

# Calcular un IC de del 95% mediante los percentiles 0.025 y 0.975 
percentil_025 = np.percentile(sample_prop_doctorado, 2.5)
percentil_975 = np.percentile(sample_prop_doctorado, 97.5)

#Resultados
print(f"Media de las proporciones de doctorados en las muestras: {np.mean(sample_prop_doctorado)}")
print(f"Percentil 2.5: {percentil_025}")
print(f"Percentil 97.5: {percentil_975}")

# Graficar la densidad con las medias de los conjuntos y el IC del 95%
plt.figure(figsize=(10, 6))
sns.kdeplot(sample_prop_doctorado, fill=True, color='skyblue', alpha=0.5, label='Densidad de las medias')
#plt.axvline(np.mean(sample_prop_doctorado), color='red', linestyle='dashed', linewidth=2, label='Media')
plt.axvline(percentil_025, color='blue', linestyle='solid', linewidth=2, label='Percentil 2.5')
plt.axvline(percentil_975, color='blue', linestyle='solid', linewidth=2, label='Percentil 97.5')
plt.xlabel('Proporción de Doctorado')
plt.ylabel('Densidad')
plt.title('Distribución de las medias de las proporciones de doctorados en las muestras')
plt.legend()
plt.show()

#-------------BOOSTRAP PARA PRUEBA DE HIPOTESIS-----------
#Calcular la diferencia observada
doctorado_df = df[df['grado'] == 'Doctorado']
#Proporción de doctorado por género
prop_doctorado_por_genero = doctorado_df.groupby('Género').size() / df.groupby('Género').size()
# Restar las proporciones
diff_prop_doctorado = prop_doctorado_por_genero['Masculino'] - prop_doctorado_por_genero['Femenino']

# Crear una lista para almacenar los resultados
resultados_list = []

# Mediante bootstrap generar 500 conjuntos con h0 como cierta
sample_diff_doctorado = []
for i in range(500):
    # Realizar un remuestreo de los datos
    muestra = df.copy()
    muestra['grado'] = np.random.permutation(muestra['grado'])
    
    # Calcular la diferencia entre géneros en los conjuntos generados
    prop_doctorado_masculino = muestra[muestra['Género'] == 'Masculino']['grado'].eq('Doctorado').mean()
    prop_doctorado_femenino = muestra[muestra['Género'] == 'Femenino']['grado'].eq('Doctorado').mean()
    diff_doctorado_muestra = prop_doctorado_masculino - prop_doctorado_femenino
    
    sample_diff_doctorado.append(diff_doctorado_muestra)
    
    # Agregar los resultados a la lista
    resultados_list.append({'Número de muestra': i + 1, 'Diferencia de doctorado entre géneros': diff_doctorado_muestra})

# Imprimir la media de las diferencias entre géneros en las muestras
print(f"Media de las diferencias de doctorado entre géneros en las muestras: {np.mean(sample_diff_doctorado)}")

# Convertir la lista de resultados en un DataFrame
resultados = pd.DataFrame(resultados_list)

# Imprimir el DataFrame con los resultados
print(resultados)

#Calcular un IC del 95% mediante los percentiles 
percentil_025 = np.percentile(sample_diff_doctorado, 2.5)
percentil_975 = np.percentile(sample_diff_doctorado, 97.5)


# Graficar la densidad con las diferencias de proporciones de los conjuntos, la diferencia observada y el IC del 95%
plt.figure(figsize=(10, 6))
sns.kdeplot(sample_diff_doctorado, fill=True, color='skyblue', alpha=0.5) #, label='Densidad de las diferencias de proporciones')
plt.axvline(diff_prop_doctorado, color='red', linestyle='dashed', linewidth=2, label='Diferencia observada')
plt.axvline(percentil_025, color='blue', linestyle='solid', linewidth=2, label='Percentil 2.5')
plt.axvline(percentil_975, color='blue', linestyle='solid', linewidth=2, label='Percentil 97.5')
#plt.xlabel('Diferencia de Doctorado entre Géneros')
plt.ylabel('Densidad')
plt.title('Distribución de las diferencias de doctorado entre géneros en las muestras')
plt.legend()
plt.show()


#--------------------- BOXPLOT------------------
suma_citas_por_departamento = df.groupby("Universidad")["Citas"].sum()


top_citas = suma_citas_por_departamento.sort_values(ascending=False).head(5).index.values

df_top_citas = df[df["Universidad"].isin(top_citas)]

# Crear el gráfico de caja
sns.boxplot(
    y="Universidad",
    x="Citas",
    data=df_top_citas,
    orient="h"
)

#-----------------------------Correlación---------------------------------
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = df.set_index('Institución')

sns.set(style='white')

def corrfunc(x, y, **kws):
  r, p = stats.spearmanr(x, y)#Pearson o spearman
  p_stars = ''
  if p <= 0.05:
    p_stars = '*'
  if p <= 0.01:
    p_stars = '**'
  if p <= 0.001:
    p_stars = '***'
  ax = plt.gca()
  ax.annotate('r = {:.2f} '.format(r) + p_stars,
              xy=(0.05, 0.9), xycoords=ax.transAxes)

def annotate_colname(x, **kws):
  ax = plt.gca()
  ax.annotate(x.name, xy=(0.05, 0.9), xycoords=ax.transAxes,
              fontweight='bold')
  
def cor_matrix(df):
  g = sns.PairGrid(df, palette=['red'])
  g.map_upper(sns.regplot, scatter_kws={'s':10})
  g.map_diag(sns.histplot, kde=True, kde_kws=dict(cut=3), alpha=.4, edgecolor=(1, 1, 1, .4))
  g.map_diag(annotate_colname)
  g.map_lower(sns.kdeplot, cmap='Blues_d')
  g.map_lower(corrfunc)
  for ax in g.axes.flatten():
    ax.set_ylabel('')
    ax.set_xlabel('')
  return g

cor_matrix(df)

#----------------------------ODDS RATIO---------------------------------------
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt

# Crear la tabla de contingencia
tabla_contingencia = pd.DataFrame({
    'NoDoc': [100, 106],
    'Doctorado': [611, 255]
}, index=['Masculino', 'Femenino'])

# Realizar la prueba de odds ratio
odds_ratio, p_value = fisher_exact(tabla_contingencia)

# Mostrar los resultados
print(f"Odds Ratio: {odds_ratio}")
print(f"P-Value: {p_value}")

df_plot = pd.DataFrame({
    'Género': ['Masculino', 'Masculino', 'Femenino', 'Femenino'],
    'Grado': ['No doctorado', 'Doctorado', 'No doctorado', 'Doctorado'],
    'Counts': [100, 611, 106, 255]
})

# Calcular proporciones
df_plot['Proporción'] = df_plot.groupby('Género')['Counts'].transform(lambda x: x / x.sum() * 100)

# Crear el gráfico con matplotlib
fig, ax = plt.subplots()
colors = {'No doctorado': '#f70000', 'Doctorado': '#01f702'}

for label, data in df_plot.groupby('Grado'):
    data.plot(kind='bar', x='Género', y='Proporción', ax=ax, label=label, color=colors[label])

plt.title('Grado académico por género')
plt.xlabel('Género')
plt.ylabel('Proporción')
plt.legend(title='Grado académico', facecolor='white', framealpha=1)
plt.show()

#---------------------Prueba T-test, Mann-Whitney---------------
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon, ttest_ind
import matplotlib.pyplot as plt

data = {
    'Género': ['Masculino'] * 50 + ['Femenino'] * 50,
    'Numero': list(range(50)) + list(range(50, 100))
}

BaseNumeroslong = pd.DataFrame(data)

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.boxplot(x='Género', y='Numero', data=BaseNumeroslong, palette="Set2")
plt.xlabel('Género', fontsize=14, fontweight='bold')
plt.ylabel('Número de investigadores/as', fontsize=14, fontweight='bold')
plt.title('Gráfico de cajas por género', fontsize=16, fontweight='bold')
plt.show()

#Pruebas paramétrica o no paramétrica dependiendo de la normalidad
# Prueba de Wilcoxon 
statistic_wilcoxon, p_value_wilcoxon = wilcoxon(
    BaseNumeroslong[BaseNumeroslong['Género'] == 'Masculino']['Numero'],
    BaseNumeroslong[BaseNumeroslong['Género'] == 'Femenino']['Numero']
)

# Prueba t de Student (paramétrica)
statistic_ttest, p_value_ttest = ttest_ind(
    BaseNumeroslong[BaseNumeroslong['Género'] == 'Masculino']['Numero'],
    BaseNumeroslong[BaseNumeroslong['Género'] == 'Femenino']['Numero']
)

# Mostrar resultados
print(f"Prueba de Wilcoxon - Estadístico: {statistic_wilcoxon}, Valor p: {p_value_wilcoxon}")
print(f"Prueba t de Student - Estadístico: {statistic_ttest}, Valor p: {p_value_ttest}")

#-----------------RANGO CON SIGNO DE WILCOXON DE UNA MUESTRA------------------------
import seaborn as sns
from scipy.stats import wilcoxon, ttest_1samp
import matplotlib.pyplot as plt

# Visualización histograma y valor a comparar
plt.figure(figsize=(10, 6))
sns.histplot(df['Femenino'], color='magenta', alpha=0.4, bins=10)
plt.axvline(x=0.50, color='black', linestyle='dashed', linewidth=1)
plt.xlabel('Femenino', fontsize=14, fontweight='bold')
plt.title('Histograma con línea central', fontsize=16, fontweight='bold')
plt.show()

# Prueba de Wilcoxon (no paramétrica)
statistic_wilcoxon, p_value_wilcoxon = wilcoxon(df['Femenino'] - 0.50)

# Prueba t de una muestra (paramétrica)
statistic_ttest, p_value_ttest = ttest_1samp(df['Femenino'], 0.50)

# Mostrar resultados
print(f"Prueba de Wilcoxon - Estadístico: {statistic_wilcoxon}, Valor p: {p_value_wilcoxon}")
print(f"Prueba t de una muestra - Estadístico: {statistic_ttest}, Valor p: {p_value_ttest}")

