pd.to_numeric(df_personas['salario'].str.replace(',', ''), errors='coerce') #Quitar coma del salario 2,000 -> 2000

#Encontrar valores fuera de rango
citas_values = df['Citas'].values

assert np.all((citas_values >= 0) & (citas_values <= 500)), "No todos los valores están en el rango [0, 500]"

#reemplazar los valores fuera de rango por valor o NA
df['precio'] = df['precio'].where((df['precio'] >= 0) & (df['precio'] <= 5000), other=None)
df

#++++++++++++++++++++++Fechas++++++++++++++++++++++
#verificar si todas la fechas están en pasado
from datetime import datetime 

df['fecha'] = pd.to_datetime(df['fecha'])  # Asegúrate de que la columna 'fecha' sea de tipo datetime

assert (df['fecha'] <= pd.to_datetime(datetime.now().date())).all(), "Not all dates are in the past"

#fechas fuera de rango 
df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')  
df[df['fecha'] > datetime.now()]


#++++++++++++++++++++++Duplicados++++++++++++++++++++++
df.duplicated().sum() #Cuantas filas están duplicadas
df[df.duplicated()]  #ver las filas duplicadas
df = df.drop_duplicates() ##eliminar filas duplicadas

#filas parcialmente duplicadas
df_duplicados = df.groupby(['nombre', 'apellido']).size().reset_index(name='n')
df_duplicados[df_duplicados['n'] > 1]

#eliminar filas parcialmente duplicadas
df.drop_duplicates(subset=['nombre', 'apellido'], keep='first') 

#eliminar filas parcialmente duplicadas pero conservando el promedio 
df.groupby(['nombre', 'apellido']).agg({'citas': 'mean'}).reset_index()

#--------------CATEGORIAS (cadenas)-------------------------------
#cambia la columna tipo a minúscula str.upper() para mayusculas
df['tipo_new'] = df['tipo'].str.lower()
df['tipo_new'].value_counts()

#elimina espacios antes y despues (no en medio)
df['tipo'] = df['tipo'].str.strip()
df['tipo'].value_counts()

# Colapsar datos similares en una nueva 
perro = ['poodle', 'labrador', 'beagle']
df['tipo'] = df['tipo'].replace(perro, 'perro')
df['tipo'].value_counts()

#--------------CADENAS-------------------------------
#ver tarjertas cuyo numero es "1234-1232-2343-2324"
import re
df[df['tarjeta'].apply(lambda x: bool(re.search('-', x)))]

#reemplaza los guiones por espacios
df['tarjeta'] = df['tarjeta'].str.replace("-", " ")
df

#eliminar - y " " y contar si son 16 digitos
df['tarjeta'].apply(lambda x: re.sub(r'[-\s]', '', x)).str.len()

#verificar si es distinta de 16
[df['tarjeta'].str.len()!= 16]

#Calcular similitud de dos cadenas 
import stringdist

cadena1 = "baboon"
cadena2 = "typhoon"

# Calcular la distancia de Levenshtein entre las dos cadenas
stringdist.levenshtein(cadena1, cadena2)

# Calcular la similitud de dos cadenas con jaccard y lcs
import textdistance

cadena1 = "baboon"
cadena2 = "typhoon"

jaccard = textdistance.jaccard(cadena1, cadena2)
lcs = textdistance.lcsstr(cadena1, cadena2)

print("Jaccard", jaccard)
print("LCS:", lcs)

#ejemplo para corregir entradas mal escritas en una encuesta
encuesta = pd.DataFrame({'city': ['mxico', 'exico', 'Mxic', 'juadalajara', 'uadalajara']})
ciudad = pd.DataFrame({'city': ['México', 'Guadalajara']})

def encontrar_ciudad_similar(ciudad_encuesta):
    distancias = ciudad['city'].apply(lambda x: stringdist.levenshtein(ciudad_encuesta, x))
    ciudad_similar = ciudad.loc[distancias.idxmin(), 'city']
    return ciudad_similar

encuesta['ciudad_correcta'] = encuesta['city'].apply(encontrar_ciudad_similar)
encuesta

#para controlar la distancia maxima del lavenshtein 
def encontrar_ciudad_similar(ciudad_encuesta):
    distancias = ciudad['city'].apply(lambda x: stringdist.levenshtein(ciudad_encuesta, x))
    distancias_validas = distancias[distancias <= 1]
    if not distancias_validas.empty:
        ciudad_similar = distancias_validas.idxmin()
        return ciudad.loc[ciudad_similar, 'city']
    else:
        return None
        
#------------------------------------------------DATOS FALTANTES------------------------------------------------
#devuelve la variable, # NAs y % de NAs
resumen_NA = pd.DataFrame({
    'variable': df.columns,
    'NAs': df.isnull().sum(),
    '% NAs': (df.isnull().mean() * 100).round(2)
})

resumen_NA

#n° de filas, #NAs y % de NAs
fila_nas = pd.DataFrame({
    'fila': df.index,
    'NAs': df.isnull().sum(axis=1),
    '% NAs': (df.isnull().mean(axis=1) * 100).round(2)
})

fila_nas

#NAs #variables % de NAs
# Tabla resumen de datos faltantes en variables
table_NAsColumna = pd.DataFrame({
    'NAs': df.isnull().sum(),
    'Variables': df.columns,
    '% NAs': (df.isnull().mean() * 100).round(2)
})

print(table_NAsColumna)

#NAs, n° de filas % de NAs
tabla_case = pd.DataFrame({
    'NAs': df.isnull().sum(axis=1),
    'Filas': df.index,
    '% NAs': (df.isnull().mean(axis=1) * 100).round(2)
})

tabla_case

#Grafica de valores faltantes en cada variable
import missingno as msno
import matplotlib.pyplot as plt

msno.matrix(df)
plt.show()

#Grafica de valores faltantes en cada fila
msno.matrix(df.T)

#Encontrar valores NA en otros formatos
formatos_alternativos = ['N/A', 'N/a', 'Desconocido']

valores_faltantes_otro_formato = df.applymap(lambda x: x in formatos_alternativos)
valores_faltantes_otro_formato.sum()

#reemplazar NAs en otro formato 
df.replace(to_replace=formatos_alternativos, value=pd.NA, inplace=True)

#reemplaza los valores donde sean = -99
df.replace(to_replace=-99, value=pd.NA, inplace=True)

#reemplaza los valores donde sean > 99
df[df > 99] = pd.NA
df

#valores faltantes no registrados

#nombre  | tiempo
#Juan    | dia
#Juan    | noche
#Diego   | dia

combinaciones = pd.MultiIndex.from_product([df['nombre'].unique(), df['tiempo'].unique()], names=['nombre', 'tiempo'])
combinaciones_df = pd.DataFrame(index=combinaciones).reset_index()
pd.merge(combinaciones_df, df, on=['nombre', 'tiempo'], how='left')

#nombre  | tiempo
#Juan    | dia
#Juan    | noche
#Diego   | dia
#Diego   | NA

# Llenar los valores faltantes hacia adelante en la columna 'name'
#nombre  | horario
#Juan    | dia
#NA      | noche
#Diego   | dia
#NA      | noche

df['nombre'].fillna(method='ffill', inplace=True)

#nombre  | horario
#Juan    | dia
#Juan    | noche
#Diego   | dia
#Diego   | noche

# Imputar valores faltantes en columnas numéricas
def impute_below_if(data, condition):
    for column in data.columns:
        if condition(data[column]):
            data[column].fillna(method='bfill', inplace=True)
impute_below_if(df, lambda x: pd.api.types.is_numeric_dtype(x))

print(df)

# Imputar valores faltantes en variables especificas
def impute_below_at(data, variables):
    for variable in variables:
        if pd.api.types.is_numeric_dtype(data[variable]):
            data[variable] = data[variable].fillna(method='bfill')
impute_below_at(df, variables=['var1', 'var2'])
df

# Imputar valores nulos hacia abajo en todas las columnas
def impute_below_all(data):
    data.fillna(method='bfill', inplace=True)

impute_below_all(df)
df