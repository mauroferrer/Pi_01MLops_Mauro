from fastapi import FastAPI, HTTPException
import pandas as pd 
from typing import Optional
import uvicorn  




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



@app.get("/get_max_duration/{year}/{plataform}/{tipo}")
def get_max_duration(year: int,plataform: str,tipo: str):
 df_total = pd.read_csv('platform_movies_scores.csv')    
 peliculas_filtradas = df_total[(df_total['release_year'] == year) & (df_total['Plataforma'] == plataform) & (df_total['duration_type'] == tipo)]
 pelicula_mas_larga = df_total.loc[peliculas_filtradas['duration_int'].idxmax()]
 return 'pelicula_mas_larga:',pelicula_mas_larga['title']





@app.get("/get_score_count/{platform}/{scored}/{year}")
def get_score_count(platform: str, scored: float, year: int):
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


@app.get("/get_actor/{platform}/{year}")
def get_actor(platform:str, year:int):
   df_total = pd.read_csv('platform_movies_scores.csv')
   #seleccionamos los registros para cada atributo
   df_filter = df_total.loc[(df_total['Plataforma']==platform) & (df_total['release_year']== year)]
   #Contamos el actor que mas se repite segun plataforma y año
   conteo_actores = df_filter['cast'].value_counts()
   #Retornamos los actores que mas se repiten segun el año y la plataforma
   return conteo_actores.idxmax()

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



if __name__ == "_main_":

    uvicorn.run(app, host="0.0.0.0", port=8000)
