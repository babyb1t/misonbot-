# MisOFF_Bot

## Descripción
uno de las grandes problemas que nos enfrentamos actualmente en la sociedad es la desigualdad de género, de allí nace el proyecto **MisOFF** contra la misoginia. 

Queremos dar herramientas tecnológicas a la ciudadanía para crear conciencia sobre el contenido misógino de algunas canciones mas escuchadas en la actualidad. Por ello surgió la idea de crear un bot de análisis de canciones, que les permita a los ciudadanos de España analizar la letra de las canciones mas escuchadas en los medios y que esto sirva para cambiar los hábitos de consumo de música entre los españoles, en consecuencia que los medios se adapten y vean en la necesidad de modificar el contenido musical que transmiten.

**El bot MisOFF** le pedirá a los usuarios, que les indiquen cuales estrofas de la canción poseen algún contenido referente a una de las siguientes preguntas, estereotipos, roles, poder, cuerpo y sexismo. en caso de indicar una o mas estrofas se te pedirá que indiques el grado de ofensa o agresión que representa dicha estrofa. 

## Guía de uso.
primero se tiene que ejecutar el script songdb para generar una base de datos en mongodb, luego ejecutad el script MisOFF.py con llenando todas las variables de el script variables.py. 

## Equipo

- Autor:
  - Cancar Ricardo Miguel
- Director del proyecto:
  - [Diego Álvarez](https://about.me/diegoalsan) | @diegoalsan

## Estructura de datos:
**salida** colección users.
```
{
    "_id" : ObjectId(x),
    "update_id" : xxxxxx,
    "user_id" : xxxx,
    "user_age" : xxxxx,
    "date" : xxxxx,
    "Sexo" : "xxxx",
    "Codigo_sexo" : x,
    "analisis" : [	{
			"name" : "xxxx",
			"genero" : "xxxx",
			"Codigo_cancion" : xxxxx,
			"codigo_parrafo_estereotipo" : [x,x,x],
			"Grado_estereotipo" : xxxx,
			"codigo_parrafo_roles" :[x,x,x],
			"Grado_roles" :xxxx,
			"codigo_parrafo_poder" : [x,x,x],
			"Grado_poder" : xxx,
			"codigo_parrafo_cuerpo" : [x,x,x],
			"Grado_cuerpo" : xxxx,
			"Pregunta_general" : xxxx,
			"Grado_general" : xxxx
		}, ..., ..., ... ]
}

```



## Contexto del proyecto

El trabajo que contiene este repositorio se ha desarrollado en el [**Àrea Hackers cívics**](http://civichackers.cc). Un espacio de trabajo colaborativo formado por [hackers cívics](http://civichackers.webs.upv.es/conocenos/que-es-una-hacker-civicoa/) que buscamos y creamos soluciones a problemas que impiden que los ciudadanos y ciudadanas podamos influir en los asuntos que nos afectan y, así, construir una sociedad más justa. En definitiva, abordamos aquellos retos que limitan, dificultan o impiden nuestro [**empoderamiento**](http://civichackers.webs.upv.es/conocenos/una-aproximacion-al-concepto-de-empoderamiento/).

El [**Àrea Hackers cívics**](http://civichackers.cc) ha sido impulsada por la [**Cátedra Govern Obert**](http://www.upv.es/contenidos/CATGO/info/). Una iniciativa surgida de la colaboración entre la Concejalía de Transparencia, Gobierno Abierto y Cooperación del Ayuntamiento de València y la [Universitat Politècnica de València](http://www.upv.es).

  ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/Logo_CGO_web.png) ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/logo_AHC_web.png)



