#!/bin/bash

##------------------------------------------------------------------------
## script bash exporta colecciones a archivos csv.
##------------------------------------------------------------------------

mongoexport  --db users --collection users --type=csv  --out  input/userspre.csv --fields update_id,user_id,user_age,Sexo,Codigo_sexo,analisis



mongoexport  --db song --collection regueton --type=csv  --out  input/raw_regueton.csv --fields _id,Name_song,Genero,Artista,user_id,user_age,analisis,valid,Lyrics

mongoexport  --db song --collection pop --type=csv  --out  input/raw_pop.csv --fields _id,Name_song,Genero,Artista,user_id,user_age,analisis,valid,Lyrics

mongoexport  --db song --collection romantica --type=csv  --out  input/raw_romantica.csv --fields _id,Name_song,Genero,Artista,user_id,user_age,analisis,valid,Lyrics


mongoexport  --db song --collection pop_es --type=csv  --out  input/raw_pop_es.csv --fields _id,Name_song,Genero,Artista,user_id,user_age,analisis,valid,Lyrics

mongoexport  --db song --collection allsongs --type=csv  --out  input/allsongs.csv --fields _id,estrofa

mkdir output
