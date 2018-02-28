#!/usr/bin/python3

import re
import sys
import variables
from pymongo import MongoClient
from random import randint

##------------------------------------------------------------------------
## conexión MongoDB
##------------------------------------------------------------------------

try:
  #client = MongoClient('localhost',27017)
  client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("- Error al conectarse a la BD de MongoDB: ") 

##------------------------------------------------------------------------
## variables globales para acceder a las colecciones de que están 
## almacenadas en la base de datos
##------------------------------------------------------------------------
 
db = client.song
tmp = db.tmp

# devuelve una colección segun el género seleccionado. 
def musical_genre(select):
  global  db
  init = 0
  if select == 'pop':
    genero = db.pop
    init = 20000
  if select == 'reguetón':
    genero = db.regueton
    init = 10000
  if select == 'romántica':
    genero = db.romantica
    init = 30000
  return genero, init


def song_name(update):
  #funcion que de vuelve el nombre de la canción que está siendo análisada. 
  try:
    song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
    genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
    name = genero.find_one({"_id":song_id})["Name_song"]
  except Exception as e:
      logging.exception("No se pudo obtener el nombre de la canción") 

  return name


def new_song(update): 
  global tmp
  #escoge una cancion que nunca a sido analizada y devuelve 0 si es exitosa y uno si toda la base de datos fue análisada.
  anterior_songId = 0
  analyzed = 1
  
  if tmp.find({"user_id":update.message.chat.id}).count()>0:
     anterior_songId = tmp.find_one({"user_id":update.message.chat.id})["songId"]
  drop(update)
  try:
    tmp.insert({"user_id":update.message.chat.id,
              "genero":update.message.text})
  except Exception as e:
      logging.exception("no se pudo insertar datos temporales usuario.") 
  genero, init = musical_genre(update.message.text)
  i=0
  
  while  analyzed: #mientras este analizada la cancion buscara otra
    
    song_id = randint(init,init + genero.find().count() - 1)
    
    i+=1
    if i == 40:
      return 1

    try:  
      users_id = genero.find_one({'_id':song_id})["user_id"]
      valid = genero.find_one({'_id':song_id})["valid"]
    except Exception as e:
      logging.exception("no se pudo encontrar la cancion") 
   
    if valid !=1:
      analyzed=0
      for user_id in users_id:
        if user_id == update.message.chat.id or song_id == anterior_songId:
           analyzed = 1  
      if analyzed == 0:
        try:
          tmp.update({"user_id":update.message.chat.id},{"$set":{"songId":song_id}})
          tmp.update({"user_id":update.message.chat.id},{"$set":{"estro":[]}})
          return 0
        except Exception as e:
          logging.exception("no se pudo actualizar id y respuesta usuario") 
         

def insert_estrofas(update):
  #guarda las respuesta del usuario de forma temporal. 
  global tmp
  try:
    tmp.update({"user_id":update.message.chat.id},{"$push":{"estro":int(update.message.text)}})
  except Exception as e:
      logging.exception("no se pudo actualizar respuesta del usuario temporal")


def insert_general(update):
  #guarda las respuesta del usuario de forma temporal. 
  global tmp
  try:
    tmp.update({"user_id":update.message.chat.id},{"$set":{"general":update.message.text}})
  except Exception as e:
      logging.exception("no se pudo actualizar repuesta del usuario en géneral")

def num_estrofas(update):
  #guarda las respuesta del usuario de forma temporal. 
  global tmp
  return len(tmp.find_one({"user_id":update.message.chat.id})["estro"])

def analyzed(update):
  global tmp
  # indica que el usuario analizo la canción cuando el usuario contesto la ultima pregunta.  
  usuarios = client.users.users
  song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
  genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
  age = usuarios.find_one({"user_id":update.message.chat.id})["user_age"]
  try:
    genero.update({"_id":song_id},{"$addToSet":{"user_id":update.message.chat.id}})
    genero.update({"_id":song_id},{"$push":{"user_age":{"$each":[int(age)]}}})
    genero.update({"_id":song_id},{"$inc":{"analisis":1}})
  except Exception as e:
      logging.exception("no se pudo actualizar datos de la canción")
  data = genero.find_one({"_id":song_id})["analisis"]
  # si 5 usuarios diferentes terminan de analizar esta cancion la da por validad.
  
  if data > 5:
    genero.update({"_id":song_id},{"$set":{"valid":1}})

def drop(update):
   global tmp
   #elimina los datos temporales del usuario.
   db.tmp.remove({"user_id":update.message.chat.id})

def reader(update):
   global tmp
   #devuelve la letra de la canción que el usuario escogio análizar.
   song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
   genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
   
   data = genero.find_one({"_id":song_id})["Lyrics"]
   
   return data

def sanity(update):
    global tmp
    if tmp.find({"user_id":update.message.chat.id}).count() > 0:
        return True
    else:
        return False 

#función que devuelve la letra de de coro estrofa precoro y outro y su valor clave.
def lyrics(update):
   
   letra = {}
   keys = list()

   data = reader(update)
   #print(data)
   lista = re.findall(r"(?<=])[ê!-?'¡¿\s,a-zA-Z()áéíóúÁÉÍÓÚñÑçã]*",data)
   titulos = re.findall(r"\[[çã!-?'¡¿\s,a-zA-Z()áéíóúÁÉÍÓÚñÑ]+\]",data)
   for i in range(len(lista)):
      if not titulos[i] in letra:
         letra[titulos[i]] = lista[i]
         tag=re.findall(r"(outro|intro|Translation|instrumental|(\[en\]))",titulos[i], flags = re.I)
         if tag == []:
           keys.append(titulos[i])
   
   return letra , keys



