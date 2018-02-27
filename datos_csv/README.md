# Mongodb to CSV.

## Descripción.
Este repositorio convierte los datos almacenados en mongo a csv.

## Guía de uso.
para la transformación de datos se deben ejecuatar los script en el siguiente orden.

- mongo_to_csv.sh
- mongo_r_to_csv_r.py
- genero.py
- cancione_genero.py
- todas_las_canciones.py


## estructura de datos csv.
**Parrafos_estereotipo.csv**:


  | user_id | user_age | sexo | codigo_sexo | nombre_cancion | codigo_cancion | codigo_parrafo_estereotipo | Grado_estereotipo |

**Parrafos_roles.csv**:


  | user_id | user_age | sexo | codigo_sexo | nombre_cancion | codigo_cancion | codigo_parrafo_roles | Grado_roles |


**Parrafos_poder.csv**:


  | user_id | user_age | sexo | codigo_sexo | nombre_cancion | codigo_cancion | codigo_parrafo_poder | Grado_poder |


**Parrafos_cuerpo.csv**:


  | user_id | user_age | sexo | codigo_sexo | nombre_cancion | codigo_cancion | codigo_parrafo_cuerpo | Grado_cuerpo |


**Parrafos_general.csv**:


  | user_id | user_age | sexo | codigo_sexo | nombre_cancion | codigo_cancion | codigo_parrafo_general | Grado_general |


- user_id: la identidad de usuario asignada por telegram.
- user_age: edad indicada por el usuario.
- sexo:: indicado por el usuario.
- codigo_sexo: variable categórica 0 indica que es chico y 1 indica que es chica.
- codigo_cancion: código de la letra canción almacenada en la base de datos.
- codigo_parrafo_XXXX: indicas los párrafos con un contenido relacionado a XXXX donde XXXX puede ser estereotipo, roles, poder, cuerpo o general.
- Grado_XXX: indica en una escala del 1 al 10 siendo 1 el nivel más bajo y 10 el mas alto, que tan ofensivo es dichas estrofas señaladas. 

**pop.csv**:


  | codigo_cancion | Name_song | Genero | Artista | user_id | user_age | analisis | valid |


**regueton.csv**:


  | codigo_cancion | Name_song | Genero | Artista | user_id | user_age | analisis | valid |


**romantica.csv**:


  | codigo_cancion | Name_song | Genero | Artista | user_id | user_age | analisis | valid |


- codigo_cancion: código de la letra canción almacenada en la base de datos.
- Name_song: nombre de la canción.
- Genero: género de la canción.
- Artista: interprete de la canción.
- user_id: la identidad de usuario asignada por telegram.
- user_age: edad indicada por el usuario.
- análisis: número de usuarios que han analizado dicha canción.
- valid: da por analizada una canción si suficientes usuarios han analizado dicha canción. 


**todas_canciones.csv**:


  | codigo_cancion | Numero de estrofa | Texto de estrofa |


- codigo_cancion: código de la letra canción almacenada en la base de datos.
- Numero de estrofa: le asigna un numero a la estrofa.
- Texto de estrofa: texto contenido en dicha estrofa.

## Equipo

- Autor:
  - Cancar Ricardo Miguel
- Director del proyecto:
  - [Diego Álvarez](https://about.me/diegoalsan) | @diegoalsan



## Contexto del proyecto

El trabajo que contiene este repositorio se ha desarrollado en el [**Àrea Hackers cívics**](http://civichackers.cc). Un espacio de trabajo colaborativo formado por [hackers cívics](http://civichackers.webs.upv.es/conocenos/que-es-una-hacker-civicoa/) que buscamos y creamos soluciones a problemas que impiden que los ciudadanos y ciudadanas podamos influir en los asuntos que nos afectan y, así, construir una sociedad más justa. En definitiva, abordamos aquellos retos que limitan, dificultan o impiden nuestro [**empoderamiento**](http://civichackers.webs.upv.es/conocenos/una-aproximacion-al-concepto-de-empoderamiento/).

El [**Àrea Hackers cívics**](http://civichackers.cc) ha sido impulsada por la [**Cátedra Govern Obert**](http://www.upv.es/contenidos/CATGO/info/). Una iniciativa surgida de la colaboración entre la Concejalía de Transparencia, Gobierno Abierto y Cooperación del Ayuntamiento de València y la [Universitat Politècnica de València](http://www.upv.es).

  ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/Logo_CGO_web.png) ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/logo_AHC_web.png)




