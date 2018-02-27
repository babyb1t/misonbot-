# MisOFF_Bot extracción y alamcenamiento 

## Descripción

Este repositorio contiene los scripts que recolectan las letras de canciones que son almacenadas en una base de datos mongo. Este codigo puede ser utilizado por cualquier persona que tenga el token de genius 

### Herramientas
Python 3.6.0

LIBRERÍAS EN PYTHON
- MongoClient
- Json
- BeautifulSoup

## estructura de datos.

Al ejecutar el **script songdb.py** se se almacenan una lista de canciones divididas en tres géneros.

-reguetón
-pop
-romántica


**salidad** colección = pop, romántica, reguetón.
```
 {_id:xxxx,
  Name_song:xxxxx,
  Artista: xxxxx,
  user_id:[xxxx, xxxx, xxxx, ...]
  user_age:[xxxx, xxxx, xxxx, ...]
  analisis:x
  valid:
  Lyrics:
 }
```
la **_id** de la colección indica el género es decir, si la id comienza en 1 son letras de canciones de reguetón, cuando comienza en 2 son letras de canciones de pop, si comienza en 3 son letras de canciones románticas. 

**el script allsong_collection.py** genera una colección de de todas las canciones almacenadas en la base de datos.

**salidad** colección allsong

```
 {_id:xxxx,
  estrofa:xxxx
 }

```
donde la _id es la id de la canción
estrofas letra de la canción dividida por estrofas 

## Equipo

- Autor:
  - Cancar Ricardo Miguel
- Director del proyecto:
  - [Diego Álvarez](https://about.me/diegoalsan) | @diegoalsan


## Contexto del proyecto

El trabajo que contiene este repositorio se ha desarrollado en el [**Àrea Hackers cívics**](http://civichackers.cc). Un espacio de trabajo colaborativo formado por [hackers cívics](http://civichackers.webs.upv.es/conocenos/que-es-una-hacker-civicoa/) que buscamos y creamos soluciones a problemas que impiden que los ciudadanos y ciudadanas podamos influir en los asuntos que nos afectan y, así, construir una sociedad más justa. En definitiva, abordamos aquellos retos que limitan, dificultan o impiden nuestro [**empoderamiento**](http://civichackers.webs.upv.es/conocenos/una-aproximacion-al-concepto-de-empoderamiento/).

El [**Àrea Hackers cívics**](http://civichackers.cc) ha sido impulsada por la [**Cátedra Govern Obert**](http://www.upv.es/contenidos/CATGO/info/). Una iniciativa surgida de la colaboración entre la Concejalía de Transparencia, Gobierno Abierto y Cooperación del Ayuntamiento de València y la [Universitat Politècnica de València](http://www.upv.es).

  ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/Logo_CGO_web.png) ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/logo_AHC_web.png)



