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
#------------------------------Grafica de pastel con etiquetas------------
# group countries by continents and apply sum() function 
df_continents = df_can.groupby('Continent', axis=0).sum()

# note: the output of the groupby method is a `groupby' object. 
# we can not use it further until we apply a function (eg .sum())
print(type(df_can.groupby('Continent', axis=0)))

df_continents.head()

# autopct create %, start angle represent starting point
df_continents['Total'].plot(kind='pie',
                            figsize=(5, 6),
                            autopct='%1.1f%%', # add in percentages
                            startangle=90,     # start angle 90° (Africa)
                            shadow=True,       # add shadow      
                            )

plt.title('Immigration to Canada by Continent [1980 - 2013]')
plt.axis('equal') # Sets the pie chart to look like a circle.
plt.legend(labels=df_continents.index, loc='upper left') 


plt.show()
#-------------------------Grafica de pastel con una porcion resaltada------------
fig,ax=plt.subplots()

#Pie on immigrants
ax.pie(total_immigrants[0:5], labels=years[0:5], 
       colors = ['gold','blue','lightgreen','coral','cyan'],
       autopct='%1.1f%%',explode = [0,0,0,0,0.1]) #using explode to highlight the lowest 

ax.set_aspect('equal')  # Ensure pie is drawn as a circle

plt.title('Distribution of Immigrants from 1980 to 1985')
#plt.legend(years[0:5]), include legend, if you donot want to pass the labels
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
#-----------------------------------------Grafica de áreas -----------------------------------------
df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)

# get the top 5 entries
df_top5 = df_can.head()

# transpose the dataframe
df_top5 = df_top5[years].transpose()

df_top5.head()

# Cambiamos los valores del índice de df_top5 a tipo entero para poder graficar
df_top5.index = df_top5.index.map(int)

# Graficamos el DataFrame utilizando un gráfico de área no apilado con un tamaño de figura de 20x10
df_top5.plot(kind='area', 
             stacked=False, 
             figsize=(20, 10))  # se pasa una tupla (x, y) para el tamaño

# Establecemos el título del gráfico y las etiquetas de los ejes
plt.title('Tendencia de Inmigración de los 5 Principales Países')
plt.ylabel('Número de Inmigrantes')
plt.xlabel('Años')

# Mostramos el gráfico
plt.show()

#----------------------------------------Grafica de barras con anotaciones------
# step 1: get the data
df_iceland = df_can.loc['Iceland', years]
df_iceland.head()

df_iceland.plot(kind='bar', figsize=(10, 6), rot=90)

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Icelandic Immigrants to Canada from 1980 to 2013')

# Annotate arrow
plt.annotate('',  # s: str. will leave it blank for no text
             xy=(32, 70),  # place head of the arrow at point (year 2012 , pop 70)
             xytext=(28, 20),  # place base of the arrow at point (year 2008 , pop 20)
             xycoords='data',  # will use the coordinate system of the object being annotated
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
             )

# Annotate Text
plt.annotate('2008 - 2011 Financial Crisis',  # text to display
             xy=(28, 30),  # start the text at at point (year 2008 , pop 30)
             rotation=72.5,  # based on trial and error to match the arrow
             va='bottom',  # want the text to be vertically 'bottom' aligned
             ha='left',  # want the text to be horizontally 'left' algned.
             )

plt.show()

#------------------------------------Graficos de burbujas -----------------------------------
# transposed dataframe
df_can_t = df_can[years].transpose()

# cast the Years (the index) to type int
df_can_t.index = map(int, df_can_t.index)

# let's label the index. This will automatically be the column name when we reset the index
df_can_t.index.name = 'Year'

# reset index to bring the Year in as a column
df_can_t.reset_index(inplace=True)

# view the changes
df_can_t.head()

# normalize Brazil data
norm_brazil = (df_can_t['Brazil'] - df_can_t['Brazil'].min()) / (df_can_t['Brazil'].max() - df_can_t['Brazil'].min())

# normalize Argentina data
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())

# Brazil
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,  # transparency
                    color='green',
                    s=norm_brazil * 2000 + 10,  # pass in weights 
                    xlim=(1975, 2015)
                    )

# Argentina
ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Argentina',
                    alpha=0.5,
                    color="blue",
                    s=norm_argentina * 2000 + 10,
                    ax=ax0
                    )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from Brazil and Argentina from 1980 to 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')
#----------------------------------------WORD CLOUDS-----------------------------
# Importa el paquete WordCloud y el conjunto de palabras vacías (stopwords)
from wordcloud import WordCloud, STOPWORDS

print('¡Wordcloud importado!')

import urllib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Abre el archivo y léelo en una variable llamada alice_novel
alice_novel = urllib.request.urlopen('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/alice_novel.txt').read().decode("utf-8")

# Crea un conjunto de palabras vacías a partir del conjunto predefinido de STOPWORDS
stopwords = set(STOPWORDS)

# Si obtienes un error de atributo al generar la nube de palabras, actualiza Pillow y numpy usando el siguiente código
%pip install --upgrade Pillow 
%pip install --upgrade numpy

# Crea un objeto WordCloud
alice_wc = WordCloud()

# Genera la nube de palabras
alice_wc.generate(alice_novel)

# Muestra la nube de palabras
plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')  # Oculta los ejes
plt.show()

# Configura el tamaño de la figura para la visualización
fig = plt.figure(figsize=(14, 18))

# Muestra nuevamente la nube de palabras con el tamaño de figura configurado
plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')  # Oculta los ejes
plt.show()

# Añade la palabra 'said' al conjunto de palabras vacías
stopwords.add('said')

# Regenera la nube de palabras excluyendo la nueva palabra vacía
alice_wc.generate(alice_novel)

# Muestra la nube de palabras con la palabra 'said' excluida
fig = plt.figure(figsize=(14, 18))

plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')  # Oculta los ejes
plt.show()

# Guarda una máscara de imagen de la nube de palabras en la variable alice_mask
alice_mask = np.array(Image.open(urllib.request.urlopen('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/alice_mask.png')))

# Configura el tamaño de la figura para la visualización de la máscara
fig = plt.figure(figsize=(14, 18))

# Muestra la máscara de la nube de palabras en escala de grises
plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')  # Oculta los ejes
plt.show()

# Crea un nuevo objeto WordCloud con fondo blanco, máximo de 2000 palabras, máscara de imagen y palabras vacías
alice_wc = WordCloud(background_color='white', max_words=2000, mask=alice_mask, stopwords=stopwords)

# Genera la nube de palabras con la nueva configuración
alice_wc.generate(alice_novel)

# Muestra la nube de palabras con la configuración nueva
fig = plt.figure(figsize=(14, 18))

plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')  # Oculta los ejes
plt.show()
#-------------------------------- MAPAS GEOGRAFICO CON ETIQUETAS-------------
   import numpy as np  # útil para muchos cálculos científicos en Python
import pandas as pd # biblioteca principal para estructuras de datos

# Instalación e importación de la biblioteca folium para visualización de mapas
#!pip3 install folium==0.5.0
import folium

print('¡Folium instalado e importado!')

# Definir las coordenadas de latitud y longitud de México
mexico_latitude = 23.6345 
mexico_longitude = -102.5528

# Definir el mapa centrado en México con un nivel de zoom mayor
mexico_map = folium.Map(location=[mexico_latitude, mexico_longitude], zoom_start=4)

# Mostrar el mapa de México
mexico_map

# Crear un mapa de Cartodb dark_matter centrado en Canadá
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Cartodb dark_matter')

# Mostrar el mapa del mundo centrado en Canadá
world_map

# Crear y mostrar el mapa de San Francisco
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Mostrar el mapa de San Francisco
sanfran_map

# Instanciar un grupo de características para los incidentes en el dataframe
incidents = folium.map.FeatureGroup()

# Bucle para agregar los 100 crímenes al grupo de características de incidentes
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5, # definir el tamaño de los marcadores circulares
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# Agregar incidentes al mapa
sanfran_map.add_child(incidents)

# Instanciar un grupo de características para los incidentes en el dataframe (repetido)
incidents = folium.map.FeatureGroup()

# Bucle para agregar los 100 crímenes al grupo de características de incidentes (repetido)
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5, # definir el tamaño de los marcadores circulares
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# Agregar texto emergente a cada marcador en el mapa
latitudes = list(df_incidents.Y)
longitudes = list(df_incidents.X)
labels = list(df_incidents.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(sanfran_map)    
    
# Agregar incidentes al mapa
sanfran_map.add_child(incidents)

# Crear y mostrar el mapa de San Francisco
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Bucle para agregar los 100 crímenes al mapa con marcadores circulares
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.vector_layers.CircleMarker(
        [lat, lng],
        radius=5, # definir el tamaño de los marcadores circulares
        color='yellow',
        fill=True,
        popup=label,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(sanfran_map)

# Mostrar el mapa de San Francisco
sanfran_map

from folium import plugins

# Reiniciar con una copia limpia del mapa de San Francisco
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Instanciar un objeto de clúster de marcadores para los incidentes en el dataframe
incidents = plugins.MarkerCluster().add_to(sanfran_map)

# Bucle para agregar cada punto de datos al clúster de marcadores
for lat, lng, label, in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# Mostrar el mapa final con los incidentes agrupados
sanfran_map
#----------------------------- MAPAS GEOGRAFICOS CON COLORES (INTENSIDAD)Choropleth map------------------
    # Importamos la biblioteca pandas para el manejo de datos
df_can = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Canada.csv')

print('¡Datos descargados y leídos en un DataFrame!')

# Para crear un mapa coroplético (Choropleth), necesitamos un archivo GeoJSON que defina las áreas/fronteras del estado, condado o país de nuestro interés. En este caso, como queremos crear un mapa mundial, necesitamos un archivo GeoJSON que defina las fronteras de todos los países del mundo. Por conveniencia, se proporciona este archivo, así que lo descargamos y lo nombramos como world_countries.json.

# Descargar el archivo GeoJSON de los países
! wget --quiet https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json
    
print('¡Archivo GeoJSON descargado!')

# Ruta al archivo GeoJSON de los países del mundo
world_geo = r'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'

# Crear un mapa simple del mundo centrado en [0, 0] con un nivel de zoom inicial de 2
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Generar un mapa coroplético utilizando la inmigración total de cada país a Canadá desde 1980 hasta 2013
world_map.choropleth(
    geo_data=world_geo,  # Archivo GeoJSON que define las fronteras de los países
    data=df_can,         # DataFrame con los datos de inmigración
    columns=['Country', 'Total'],  # Columnas que se usarán para el mapeo
    key_on='feature.properties.name',  # Vinculación de los datos con las propiedades del GeoJSON
    fill_color='YlOrRd',  # Paleta de colores del mapa
    fill_opacity=0.7,     # Opacidad del color de relleno
    line_opacity=0.2,     # Opacidad del color de las líneas de frontera
    legend_name='Inmigración a Canadá',  # Nombre de la leyenda del mapa
    reset=True            # Reiniciar para asegurar que no se acumulen datos previos
)

# Mostrar el mapa generado
world_map
