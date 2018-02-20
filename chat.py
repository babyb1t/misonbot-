#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import read_db
import variables
from telegram import Bot
from telegram.error import NetworkError, Unauthorized
from time import sleep
from pymongo import MongoClient

client = MongoClient('localhost',27017)
#client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))


def user_sexo(update):
    db = client.users
    posts = db.users 
    posts.update({"user_id":update.message.chat.id},{"$set":{"Sexo":update.message.text}})#update.message.text
    if update.message.text == "Chico":
       posts.update({"user_id":update.message.chat.id},{"$set":{"Codigo_sexo":0,"analisis":[]}})
    else:
       posts.update({"user_id":update.message.chat.id},{"$set":{"Codigo_sexo":1,"analisis":[]}})

def user_age(update):
  db = client.users
  posts = db.users
  if posts.find({"user_id": update.message.chat.id}).count() == 0:

    post = {"update_id": update.update_id,
            "user_id": update.message.chat.id,
            "user_age": update.message.text,
            "date": update.message.date

            }
    posts.insert_one(post).inserted_id





def user_exists(update):
# revisa si el usuario a usado el bot antes, comprobando que esté en la base de datos.
  db = client.users
  posts =db.users
  if posts.find({"user_id": update.message.chat.id}).count() > 0:
   
    return True
  else:
    return False

def genero_cancion(song_id):
  if song_id >= 10000 and song_id <= 20000:
    genero = "reguetón"
  if song_id >= 20000 and song_id <= 30000:
    genero = "pop"
  if song_id >= 30000 and song_id <= 40000:
    genero = "romántica"
  return genero


def check_array(update,song_name):
  db = client.users
  posts = db.users
  bol = False
  for i in range(0,len(posts.find_one({"user_id":  update.message.chat.id})["analisis"]) ):
     if posts.find_one({"user_id":  update.message.chat.id})["analisis"][i]["name"] == song_name:
         bol = True
  return bol

def base(update,song_name):
   #genera la estructura de los datos.
   db = client.users
   posts = db.users
   songdb = client.song
   tmp = songdb.tmp
   if not check_array(update,song_name):
     posts.update_one({"user_id":  update.message.chat.id}, {"$push": {"analisis":{ "name":song_name,
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

def estereotipo(update, song_name):
  #inserta la respuesta estereotipo del usuario. 
  db = client.users
  songdb = client.song
  tmp = songdb.tmp
  posts = db.users
  
  
  if update.message.text != 'ninguna' :
    posts.update_one({"user_id":  update.message.chat.id}, {"$set": {
                     "analisis.$[elemt].codigo_parrafo_estereotipo":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                     "analisis.$[elemt].Grado_estereotipo":int(update.message.text)
                      }}, array_filters=[{"elemt.name":{"$eq":song_name}}] )           
     
  else:
    posts.update_one({"user_id":  update.message.chat.id}, {"$set": {
                         "analisis.$[elemt].codigo_parrafo_estereotipo": 0,
                         "analisis.$[elemt].Grado_estereotipo": 0
                        }}, array_filters=[{"elemt.name":{"$eq":song_name}}] ) 
  tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def roles(update,song_name):
    #inserta la respuesta roles del usuario.    
    db = client.users
    posts = db.users
    song = client.song
    tmp = song.tmp
    if update.message.text != 'ninguna':
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_roles": tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_roles":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}]  )
    else:
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_roles": 0,
                                 "analisis.$[elemt].Grado_roles":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])

    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})


def poder(update, song_name):
    #inserta la respuesta poder del usuario.
    db = client.users
    posts = db.users
    song = client.song
    tmp = song.tmp
    
    if update.message.text != 'ninguna':
       posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_poder":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_poder":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
    else:
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_poder":0,
                                 "analisis.$[elemt].Grado_poder":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def cuerpo(update, song_name):
    #inserta la respuesta cuerpo del usuario.
    db = client.users
    posts = db.users
    song = client.song
    tmp = song.tmp
    if update.message.text != 'ninguna':
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_cuerpo":tmp.find_one({'user_id':update.message.chat.id})["estro"],
                                 "analisis.$[elemt].Grado_cuerpo":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
    else:
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].codigo_parrafo_cuerpo":0,
                                 "analisis.$[elemt].Grado_cuerpo":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
    tmp.update({"user_id":  update.message.chat.id},{"$set":{"estro":[]}})

def general(update, song_name ):
    #inserta la respuesta general es decir si al usuario le parecio sexista la letra de la cancion.
    db = client.users
    posts = db.users
    if update.message.text == 'No' or update.message.text == 'no':
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].Pregunta_general": 'No',
                                 "analisis.$[elemt].Grado_general":0
                                }}, array_filters=[{"elemt.name":{"$eq":song_name}}])
    else:
      posts.update_one({"user_id":  update.message.chat.id},
                       {"$set": {"analisis.$[elemt].Pregunta_general":'Si',
                                 "analisis.$[elemt].Grado_general":int(update.message.text)
                                 }}, array_filters=[{"elemt.name":{"$eq":song_name}}])



if __name__ == '__main__':
  main()
