<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps) - Mauro Ferrera'**</h1>

<p align="center">
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0wFUH9DQH-qy5ogk-PquJMxqh8TzyuyEwsDD0j_R7l-AWDTth99DUu1-VBu8QWEhjPA&usqp=CAU"  height=300>
</p>

## ¡Bienvenido/a a este proyecto donde te explicare como hacer un proceso de ETL, un analisis EDA y un modelo de ML(Machine learning) para hacer un sistema de recomendacion trabajando con plataformas de streaming  
 

<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

## Contexto
### Tenemos 4 datasets que debemos transformar para poder hacer nuestro sistema de consultas y nuestro modelo de recomendacion
#### -Datasets de Hulu
#### -Datasets de Netflix
#### -Datasets de Disney
#### -Datasets de Amazon 

<hr>  

# El rol que cumpliremos en este proyecto es de un DataSciense 

### Paso 1. **`Transformaciones de los datos(ETL)`** : 


+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

+ Una vez transformado cada datasets lo cancatenamos por su show_Id y los convertimos en un datasets
 
                 **  El codigo que puede encontrar en el archivo: 'ETL_EDA_PI_MLops.ipynb' **
<br/>

<hr>

### Paso 2. **`Desarrollamos una API`** en donde vamos a poder hacer consultas de las siguientes tipo
 ***Disponibilizamos los datos de las empresas usando el framework*** ***FastAPI***.
   ***Las consultas son las siguientes:***


+ #### **Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función va a llamarse get_max_duration(year, platform, duration_type))** 
    Esta consulta nos va a devuelve la pelicula con mayor duracion dependiendo del tipo de duracion que le demos, la plataforma que especifiquemos y el año que indiquemos
<hr>  

+ #### **Cantidad de películas por plataforma con un puntaje mayor a X en determinado año (la función debe llamarse get_score_count(platform, scored, year))**
    Esta consulta nos va a devolver la cantidad de peliculas que tengan un puntaje mayor al que le pasemos como parametro, segun la plataforma y el año
<hr> 

+ #### Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
    Esta consulta nos va a indicar la cantidad de peliculas que hay en la plataforma que indiquemos
<hr> 

+ #### Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
    Esta consulta nos devuelve el actor con mas apariciones tiene segun el año y la plataforma que pasemos como parametro
<hr> 

+ #### La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. La función debe llamarse prod_per_county(tipo,pais,anio)
     Esta consulta nos va a devolver el total de contenido de las plataformas segun el tipo(tipo de contenido movie,show TV,etc), pais que indiquemos y año 
<hr> 

+ #### La cantidad total de contenidos/productos (todo lo disponible en streaming, series, peliculas, etc) según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función debe llamarse get_contents(rating)
    Esta consulta nos va adevolver la cantidad de productos/contenido que se encuntran en las plataformas segun el tipo de rating que le pasemos por ej: 'G' = a todo publico

                 ** El codigo de las consultas para la API se encuentran en el archivo 'main.py'

<br/>

<hr>




### Paso 3. **`Análisis exploratorio de los datos`** _(Exploratory Data Analysis-EDA)_:



😉 Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior.  Nos podemos apoyar en librerías como: _pandas profiling, sweetviz, autoviz_, entre otros y sacar nuestras propias conclusiones 
                  
                   ** El codigo explicado paso a paso del analisis EDA se encuentra en el archivo 'ETL_EDA_PI_MLops.ipynb' **

<hr>

### Paso  4. Creamos el **`Sistema de recomendacion`** con un modelo de Machine learning: 

Una vez que toda la data es consumible por la API y nuestro EDA bien realizado entendiendo bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación de películas para usuarios. Éste consiste en recomendar películas a los usuarios en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán la partitura y devolverá según la lista de Python con 5 valores .luego lo implementamos implementado como una función adicional de la API anterior y debe llamarse 'get_recommendation(titulo: str)'. De ser posible, este sistema de recomendación debe ser deployado para tener una interfaz gráfica amigable para ser utilizada
**Para hacer este sistema debemos vectorizar una columna texto que va a hacer las comparaciones de palabras o caracteristicas entre las peliculas, descomponer la matriz si el archivo pesa demasiado, obtener la similitud del coseno y luego crear la funcion 'get_recommendation(titulo: str)' con la matriz que nos da la similitud del coseno**  
<br/>
                    ** Al codigo explicado paso a paso lo encontramos en el archivo, 'main.py' ** 
<hr>

### **Video explicativo de todos los pasos**



<br/>

<hr>

### **Deployemend:** 

 https://mauro-ferrera-pi-01.onrender.com/docs
