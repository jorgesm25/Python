import matplotlib.pyplot as plt
import seaborn as sns

#----------------- Grafica barras con los niveles de grado académico ordenados----
sns.set(style="whitegrid", font_scale=1.2)

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
sns.countplot(x='Grado', hue='Género', data=df, palette='pastel', dodge=True)

# Configurar etiquetas y títulos
plt.xlabel('Grado Académico', fontweight='bold')
plt.ylabel('Número de investigadores/as', fontweight='bold')
plt.title('Distribución por Grado Académico y Género', fontweight='bold')

plt.legend(title='Género', title_fontsize='12', facecolor='white')

plt.show()

#-----------------Grafica de puntos por género----------------------------------
#pasar a base log si es necesario
df['Citas_log'] = np.log(df['Citas'])
df['Articulos_log'] = np.log(df['Articulos'])

# Configurar el estilo de seaborn
sns.set(style="whitegrid", font_scale=1.2)

g = sns.scatterplot(data=df, x='Citas_log', y='Articulos_log', hue='Género', style='Género', palette='pastel', s=100, alpha=0.6)

plt.xlabel('Log(Citas)', fontweight='bold')
plt.ylabel('Log(Articulos)', fontweight='bold')
plt.title('Scatter Plot por Log(Citas) y Log(Articulos)', fontweight='bold')

g.legend(title='Género', title_fontsize='12', facecolor='white')
plt.show()

#-----------------------Mapa de calor----------------------------------
# Configurar el estilo de seaborn
sns.set(style="whitegrid", font_scale=1.2)

# Crear el gráfico de densidad bidimensional
g = sns.histplot(data=df, x='Articulos_log', y='Citas_log', hue='Género', cmap='coolwarm', cbar=True)

# Configurar etiquetas y títulos
plt.xlabel('Artículos', fontweight='bold')
plt.ylabel('Citas', fontweight='bold')
plt.title('Mapa de calor', fontweight='bold')

# Configurar leyenda
g.legend(title='Género', title_fontsize='12', facecolor='white')

# Mostrar el gráfico
plt.show()
#-------------------------Grafica de puntos-----------------------
#definir paletas de colores
colores = ["red", "green", "blue", "brown", "magenta"]

# Crear el gráfico utilizando seaborn
plt.figure(figsize=(8, 6))
scatter = sns.scatterplot(data=df, x='Pais', y='Femenino', hue='Pais', size=0.5, palette=colores)

# Añadir la media con la misma paleta de colores
means = df.groupby('Pais').mean().reset_index()
for i, row in means.iterrows():
    plt.scatter(row['Pais'], row['Femenino'], s=100, color=colores[i])

# Configuraciones adicionales del gráfico
plt.title("Porcentaje Femenino por País")
plt.xlabel("País")
plt.ylabel("Porcentaje Femenino")
plt.xticks(size=14, rotation=45, ha='right')
plt.yticks(size=14)
plt.grid(True)

# Eliminar la leyenda generada automáticamente por seaborn
scatter.legend_.remove()

# Crear manualmente la leyenda
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colores]
plt.legend(handles, df['Pais'].unique(), title='Pais')

# Mostrar el gráfico
plt.show()

#--------------------------Grafica de pastel----------------------
plt.figure(figsize=(8, 8))
plt.pie(df['Count'], labels=df['Género'], autopct='%1.1f%%', startangle=90, colors=['blue', 'pink'])

plt.axis('equal')  # Para asegurar que el gráfico sea un círculo
plt.title("Distribución de Género", fontsize=16)

plt.show()

#--------------------------Grafica de pastel por universidad---------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Filtrar por universidades únicas
universidades = df['Universidad'].unique()

# Configuraciones de estilo
colors = ['blue', 'pink']

# Crear subgráficos
fig = make_subplots(rows=1, cols=len(universidades), specs=[[{'type': 'polar'}]*len(universidades)], 
                    subplot_titles=universidades)

for i, uni in enumerate(universidades):
    df_uni = df[df['Universidad'] == uni]
    fig.add_trace(go.Barpolar(r=df_uni['Porcentaje'], theta=df_uni['Género'], 
                              marker_color=colors, 
                              marker=dict(line=dict(color='black', width=1)),
                              name=''), row=1, col=i+1)

# Configuraciones adicionales del gráfico polar con facetas
fig.update_layout(title_text='Distribución de Género por Universidad', showlegend=False)
fig.update_polars(radialaxis=dict(ticks='', showticklabels=False))

# Mostrar el gráfico
fig.show()

#---------------------Grafica de columnas para proporciones------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x='Universidad', y='Porcentaje', hue='Género')

plt.title('Distribución de Género por Universidad')
plt.xlabel('Universidad')
plt.ylabel('Porcentaje')
plt.legend(title='Género')
plt.grid(True)

plt.show()

#------------------------Grafica de probabilidad acumulada------------------------
#filtrar los datos
datos_hombres = df[df['Género'] == 'Masculino']

# Calcular la ECDF para hombres
x_hombres, y_hombres = np.sort(datos_hombres['Articulos']), np.arange(1, len(datos_hombres) + 1) / len(datos_hombres)

# ECDF para hombres
plt.plot(x_hombres, y_hombres*100, linestyle='--', lw=2)

# Etiquetar ejes y mostrar gráfico
plt.xlabel('Articulos', size=14)
plt.ylabel('ECDF', size=14)
plt.title('ECDF de articulos para Hombres', size=16)
plt.show()

#------------------------ECDF para dos grupos------------------------
#filtrar los datos
df_hombres = df[df['Género'] == 'Masculino']
citas_hombres = df_hombres['Citas']
df_mujeres = df[df['Género'] == 'Femenino']
citas_mujeres = df_mujeres['Citas']

# Calcular la ECDF para ambos
x_hombres, y_hombres = np.sort(citas_hombres), np.arange(1, len(citas_hombres) + 1) / len(citas_hombres)
x_mujeres, y_mujeres = np.sort(citas_mujeres), np.arange(1, len(citas_mujeres) + 1) / len(citas_mujeres)

# Plotear la ECDF como puntos
_ = plt.plot(x_hombres, y_hombres*100, linestyle='--', lw=2)
_ = plt.plot(x_mujeres, y_mujeres*100, linestyle='--', lw=2)

# Etiquetar ejes y mostrar gráfico
_ = plt.legend(("Hombre", "Mujer"))
_ = plt.xlabel('Citas', size=14)
_ = plt.ylabel('ECDF', size=14)
plt.show()
#------------------------Densidad----------------------------
sns.distplot(a=df.variable, color='red', 
             hist_kws={"edgecolor": 'white'})

plt.show()

#--------------------Calculo del indice H----------------------------------
# Crear un vector con los datos de las citas
citas = np.array([4, 2, 4, 1, 8, 5, 10, 2, 10, 15])

# Obtener el orden de los datos según el número de citas de mayor a menor
orden_citas = np.argsort(citas)[::-1]

# Crear un vector con las etiquetas personalizadas del eje X
etiquetas_x = [f"{i + 1}°" for i in range(len(citas))]

# Crear el gráfico de barras
plt.bar(etiquetas_x, citas[orden_citas], color='lightgray')
plt.ylim(0, 15)
plt.xlabel('Artículos ordenados por número de citas')
plt.ylabel('Número de citas')
plt.title('Cómo se calcula el índice H')
plt.xticks(rotation=45, ha='right')
plt.yticks(np.arange(0, 16, 2))

# Agregar una línea vertical
plt.axvline(x=4, color='red')

# Agregar una línea horizontal
plt.axhline(y=5, color='red')

# Mostrar el gráfico
plt.show()
#--------------------DISPERCIÓN------------------------
df_filtered = df[['Citas', 'Articulos', 'Género']].dropna(subset=['Citas', 'Articulos', 'Género'])

# Crear el gráfico de dispersión
trace = go.Scatter(
    x=df_filtered['Citas'],
    y=df_filtered['Articulos'],
    mode='markers',
    text=df_filtered['Género'],
    marker=dict(
        size=10,
        color=df_filtered['Género'].map({'Femenino': 'magenta', 'Masculino': 'blue'}),
    )
)

layout = go.Layout(
    xaxis=dict(
        title='Citas',
        gridcolor='rgba(0, 0, 0, 0.1)',  # Color de la cuadrícula
    ),
    yaxis=dict(
        title='Artículos',
        gridcolor='rgba(0, 0, 0, 0.1)',  # Color de la cuadrícula
    ),
    hovermode='closest',
    paper_bgcolor='white',  # Fondo blanco
    plot_bgcolor='white',   # Fondo blanco
    font=dict(family='Arial, sans-serif', size=12, color='black'),  # Estilo de fuente
)
fig = go.Figure(data=[trace], layout=layout)
config = {
    'displayModeBar': False, 
    'scrollZoom': False,     
    'editable': False,       
}
iplot(fig)