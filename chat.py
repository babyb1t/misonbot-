#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import read_db
import variables
import time
from telegram import Bot
from telegram.error import NetworkError, Unauthorized
from time import sleep
from pymongo import MongoClient
##------------------------------------------------------------------------
## conexión MongoDB
##------------------------------------------------------------------------
try:
  client = MongoClient('localhost',27017)
  #client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("- Error al conectarse a la BD de MongoDB: ") 

##------------------------------------------------------------------------
## variables globales para acceder a las colecciones de que están 
## almacenadas en la base de datos
##------------------------------------------------------------------------
usuarios = client.users.users
tmp = client.song.tmp



def user_sexo(update):
  ## inserta el sexo de los usuarios 
  usuarios.update({"user_id":update.message.chat.id},{"$set":{"Sexo":update.message.text}})#update.message.text
  if update.message.text == "Chico":
     usuarios.update({"user_id":update.message.chat.id},{"$set":{"Codigo_sexo":0,"analisis":[]}})
  else:
     usuarios.update({"user_id":update.message.chat.id},{"$set":{"Codigo_sexo":1,"analisis":[]}})

def user_age(update):
  ## inserta la edad de usuarios en colección users
  global usuarios
  if usuarios.find({"user_id": update.message.chat.id}).count() == 0:

    post = {"update_id": update.update_id,
            "user_id": update.message.chat.id,
            "user_age": update.message.text,
            "date": update.message.date

            }
    usuarios.insert_one(post).inserted_id





def user_exists(update):
# revisa si el usuario a usado el bot antes, comprobando que esté en la base de datos.
  global usuarios
  if usuarios.find({"user_id": update.message.chat.id}).count() > 0:
   
    return True
  else:
    return False

## los géneros están clasificados por id si la id comienza por 1 es reguetón, 2 es pop y 3 es romántica. 
def genero_cancion(song_id):
  if song_id >= 10000 and song_id <= 20000:
    genero = "reguetón"
  if song_id >= 20000 and song_id <= 30000:
    genero = "pop"
  if song_id >= 30000 and song_id <= 40000:
    genero = "romántica"
  return genero

## verifica si el usuario analizo con anterioridad dicha canción.
def check_array(update,song_name):
  global usuarios
  bol = False
  try:
    for i in range(0,len(usuarios.find_one({"user_id":  update.message.chat.id})["analisis"]) ):
       if usuarios.find_one({"user_id":  update.message.chat.id})["analisis"][i]["name"] == song_name:
           bol = True
  except Exception as e:
    logging.exception("- Error al obtener el analisis de los usuarios: ") 

  return bol


def base(update,song_name):
   #génera la estructura de los datos.
   global usuarios, tmp
   if not check_array(update,song_name):
     try:
        usuarios.update_one({"user_id":  update.message.chat.id}, {"$push": {"analisis":{ "name":song_name,
                                                                "genero":genero_cancion(tmp.find_one({'user_id':update.message.chat.id})["songId"]),
                                                                "Codigo_cancion":tmp.find_one({'user_id':update.message.chat.id})["songId"],
                                                                "codigo_parrafo_estereotipo":'',
                                                                "Grado_estereotipo":'',
                                                                "codigo_parrafo_roles":'',
                                                                "Grado_roles":'',
                                                                "codigo_parrafo_poder":'',
                                                                "Grado_poder":'',
                                                                "codigo_parrafo_cuerpo":'',
                                                                "Grado_cuerpo":'',
                                                                "Pregunta_general":'',
                                                                "Grado_general":''
                                                                                }
                                                                     }
                                                           })
     except Exception as e:
         logging.exception("no se pudo actualizar el análisis")

def estereotipo(update, song_name):
  #inserta la respuesta estereotipo del usuario. 
 
  global usuarios, tmp   
  if update.message.text != 'ninguna' :
    try:
      
      usuarios.update_one({"user_id":  update.message.chat.id}, {"$set": {
                     "analisis.$[elemt].codigo_parrafo_estereotipo":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                     "analisis.$[elemt].Grado_estereotipo":int(update.message.text)
                      }}, array_filters=[{"elemt.name":{"$eq":song_name}}] )           
    except Exception as e:
      logging.exception("no se pudo actualizar la pregunta estereotipo") 
  else:
    try:
      usuarios.update_one({"user_id":  update.message.chat.id}, {"$set": {
                         "analisis.$[elemt].codigo_parrafo_estereotipo": 0,
                         "analisis.$[elemt].Grado_estereotipo": 0
                        }}, array_filters=[{"elemt.name":{"$eq":song_name}}] ) 
    except Exception as e:
      logging.exception("no se pudo actualizar la pregunta estereotipo")
 
  tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def roles(update,song_name):
    #inserta la respuesta roles del usuario.    
    global usuarios, tmp
    if update.message.text != 'ninguna':
      try:
         usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_roles": tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_roles":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}]  )
      except Exception as e:
         logging.exception("no se pudo actualizar la pregunta roles") 
    else:
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_roles": 0,
                                 "analisis.$[elemt].Grado_roles":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
         logging.exception("no se pudo actualizar la pregunta roles") 

    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})


def poder(update, song_name):
    #inserta la respuesta poder del usuario.
    
    global usuarios, tmp
    if update.message.text != 'ninguna':
      try: 
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_poder":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_poder":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta poder") 
    else:
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_poder":0,
                                 "analisis.$[elemt].Grado_poder":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta poder") 

    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def cuerpo(update, song_name):
    #inserta la respuesta cuerpo del usuario.
    global usuarios, tmp
    if update.message.text != 'ninguna':
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_cuerpo":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_cuerpo":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta cuerpo")
 
    else:
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_cuerpo":0,
                                 "analisis.$[elemt].Grado_cuerpo":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta cuerpo") 
    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def general(update, song_name ):
    #inserta la respuesta general es decir si al usuario le parecio sexista la letra de la cancion.
    global usuarios, tmp
    if update.message.text == 'No' or update.message.text == 'no':
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].Pregunta_general": 'No',
                                 "analisis.$[elemt].Grado_general":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta general")
 
    else:
      try:
        usuarios.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].Pregunta_general":'Si',
                                 "analisis.$[elemt].Grado_general":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
      except Exception as e:
        logging.exception("no se pudo actualizar la pregunta general")   



if __name__ == '__main__':
  main()
