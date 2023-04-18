####Importamos librerias 
from fastapi import FastAPI, HTTPException #Para crear la api
import pandas as pd # Manejo de dataframes 
from typing import Optional
import uvicorn  # Para correr nuestra API
from sklearn.metrics.pairwise import cosine_similarity #Utilizamos para obtener la similitud del coseno 
from sklearn.utils.extmath import randomized_svd # Utilizamos SVD para desponer nuestra matriz 
from sklearn.feature_extraction.text import  TfidfVectorizer #Utilizamos para vectorizar datos tipo texto y convertirlos en una representacion numerica
import numpy as np # Manejo de matrices, array, etc
import sklearn 



#### IMPORTAMOS EL DATASETS CON SUS TRANSFORMACIONES HECHAS Y SUS PLATAFORMAS CONCATENADAS
df_total = pd.read_csv('platform_movies_scores.csv')

### CREACION DE API

app = FastAPI()


# introduccion
@app.get("/")
def presentacion():
    return {"PI_MLops - Mauro Ferrera"}

@app.get("/contacto")
def contacto():
    return "Email: ferreramauro05@gmail.com / Github: mauroferrer"

@app.get("/menu")
def menu():
    return "Las funciones utilizadas: get_max_duration, get_score_count, get_count_platform, get_actor, prod_per_county, get_contents "


### Consulta en donde obtenemos la pelicula que mas dura segun nuestros parametros seleccionados
@app.get("/get_max_duration/{year}/{plataform}/{tipo}")
def get_max_duration(year: int,plataform: str,tipo: str):# Definimos funcion
 df_total = pd.read_csv('platform_movies_scores.csv')    #Creamos variable con los datos
 peliculas_filtradas = df_total[(df_total['release_year'] == year) & (df_total['Plataforma'] == plataform) & (df_total['duration_type'] == tipo)] #Asignamos los valores correspondientes a cada parametro
 pelicula_mas_larga = df_total.loc[peliculas_filtradas['duration_int'].idxmax()] # Obtenemos la pelicula con mayor duracion
 return 'pelicula_mas_larga:',pelicula_mas_larga['title'] # Devolvemos solo el titulo de esa pelicula que mas dura




#Consulta nro 2
@app.get("/get_score_count/{platform}/{scored}/{year}")
def get_score_count(platform: str, scored: float, year: int): # Definimos funcion
    df_total = pd.read_csv('platform_movies_scores.csv')
    #Sleccionamos los registros que corresponden al año y al puntaje especificado
    df_filtered = df_total.loc[(df_total['release_year'] == year) & (df_total['score'] > scored)]
    #Filtrando los registro para obtener solo peliculas
    df_movies = df_filtered.loc[df_total['type'] == 'movie']
     # Filtrar los registros para obtener solo las películas que no son documentales
    df_no_doc = df_movies[~df_movies['listed_in'].str.contains('documentary', regex=False)]
     # Filtrar los registros para obtener solo las películas que se encuentran en la plataforma especificada
    df_platform = df_no_doc.loc[df_total['Plataforma'] == platform]
     # Contar el número de registros que cumplen los criterios anteriores
    count = len(df_platform)
    return count


#Consulta 3
@app.get("/get_count_platform/{platform}")
def get_count_platform(platform:str):
    df_total = pd.read_csv('platform_movies_scores.csv')
    #Seleccionamos los registros que corresponden a platform
    df_filter = df_total.loc[(df_total['Plataforma'] == platform)]
    #filtramos para obtener solo datos 'peliculas'
    df_movies = df_filter.loc[df_total['type'] == 'movie']
    #Contamos la cantidad de registros con el nombre puesto en platform 
    cantidad = df_movies['Plataforma'].value_counts()[platform]
    return cantidad.item()

#Consulta 4
@app.get("/get_actor/{platform}/{year}")
def get_actor(platform:str, year:int):
   df_total = pd.read_csv('platform_movies_scores.csv')
   #seleccionamos los registros para cada atributo
   df_filter = df_total.loc[(df_total['Plataforma']==platform) & (df_total['release_year']== year)]
   #Contamos el actor que mas se repite segun plataforma y año
   conteo_actores = df_filter['cast'].value_counts()
   #Retornamos los actores que mas se repiten segun el año y la plataforma
   return conteo_actores.idxmax()

# Consulta 5
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    df_total = pd.read_csv('platform_movies_scores.csv')
    # Comprueba si los valores de entrada son válidos y existen en DataFrame
    assert tipo.lower()  in df_total['type'].unique(), f"Invalid type of content: {tipo}"
    assert pais.lower()  in df_total['country'].unique(), f"Invalidntr couy: {pais}"
    assert anio in df_total['release_year'].unique(), f"Invalid year: {anio}"
       
    # Filtra los datos por el tipo de contenido solicitado, año y país
    filter_5 = df_total.loc[(df_total['type'] == tipo.lower() ) & 
                            (df_total['country'] == pais.lower() ) & 
                            (df_total['release_year'] == anio)]       
        
    # Comprueba si los datos filtrados están vacíos. Si no, devuelve la información deseada.
    if filter_5.empty:
        return {"pais": pais, "anio": anio, "peliculas": None}
    else:
        return {"pais": pais, "anio": anio, "peliculas": filter_5.shape[0]}


#Consulta 6
@app.get("/get_contents/{rating}")
def get_contents(rating:str):
   df_total = pd.read_csv('platform_movies_scores.csv')
   #filtramos los datos segun a su columna correspondiente
   datos_filtrados= df_total.loc[(df_total['rating'] == rating)]
   #Cotar la cantidad de veces que aparece el valor puesto como atributo en la columna 'rating'
   cantidad= datos_filtrados['rating'].value_counts()[rating]
   return cantidad.item()

#### CREACION DEL MODELO DE RECOMENDACIONES ####

user_item = df_total[['show_id', 'title','score','description']] #Utilizamos solo estas 4 columnas
user_item.reset_index(drop=True) #Reseteamos el indice
user_item = user_item.head(10000) # Cortamos los datos a 10000

#### Creamos la matriz de similitud del coseno ####

# Vectorizador TfidfVectorizer con parámetros de reduccion procesamiento
vectorizer = TfidfVectorizer(min_df=10, max_df=0.5, ngram_range=(1,2))

# Vectorizar, ajustar y transformar el texto de la columna "title" del DataFrame
X = vectorizer.fit_transform(user_item['title'])

# Calcular la matriz de similitud de coseno con una matriz reducida de 7000
similarity_matrix = cosine_similarity(X[:7000,:])

# Obtener la descomposición en valores singulares aleatoria de la matriz de similitud de coseno con 10 componentes
n_components = 10
U, Sigma, VT = randomized_svd(similarity_matrix, n_components=n_components)

# Construir la matriz reducida de similitud de coseno
reduced_similarity_matrix = U.dot(np.diag(Sigma)).dot(VT)



####Creamo la funcion utilizando la matriz 'reduce_similarity_matrix'
#Consulta 7 
@app.get('/get_recomendation/{titulo}')
def get_recommendation(titulo: str):
    try:
        #Ubicamos el indice del titulo pasado como parametro en la columna 'title' del dts user_item
        indice = np.where(user_item['title'] == titulo)[0][0]
        #Encontramos los indices de las puntuaciones y caracteristicas similares del titulo 
        puntuaciones_similitud = reduced_similarity_matrix[indice,:]
        #Ordenamos los indices de menor a mayor
        puntuacion_ordenada = np.argsort(puntuaciones_similitud)[::-1]
        #seleccionamos solo 5 
        top_indices = puntuacion_ordenada[:5]
        #retornamos los 5 items con sus titulos como una lista
        return user_item.loc[top_indices, 'title'].tolist()
        #Si el titulo dado no se encuentra damos un aviso
    except IndexError:
        print(f"El título '{titulo}' no se encuentra en la base de datos. Intente con otro título.")
 


if __name__ == "_main_":

    uvicorn.run(app, host="0.0.0.0", port=8000)
    