#!/usr/bin/python3

import re
import sys
import variables
from pymongo import MongoClient
from random import randint
client = MongoClient('localhost',27017)
#client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))

db = client.song

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
  tmp = db.tmp
  song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
  genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
  name = genero.find_one({"_id":song_id})["Name_song"]

  return name


def new_song(update): 
  #escoge una cancion que nunca a sido analizada y devuelve 0 si es exitosa y uno si toda la base de datos fue análisada.
  anterior_songId = 0
  analyzed = 1
  tmp = db.tmp
  if tmp.find({"user_id":update.message.chat.id}).count()>0:
     anterior_songId = tmp.find_one({"user_id":update.message.chat.id})["songId"]
  drop(update)
  tmp.insert({"user_id":update.message.chat.id,
              "genero":update.message.text})
  
  genero, init = musical_genre(update.message.text)
  i=0
  while  analyzed: #mientras este analizada la cancion buscara otra
    
    song_id = randint(init,init + genero.find().count() - 1)
    
    i+=1
    if i == 40:
      return 1

      
    users_id = genero.find_one({'_id':song_id})["user_id"]
    valid = genero.find_one({'_id':song_id})["valid"]
    analyzed=0
    if valid !=1:
      for user_id in users_id:
        if user_id == update.message.chat.id or song_id == anterior_songId:
           analyzed = 1  
      if analyzed == 0:
        tmp.update({"user_id":update.message.chat.id},{"$set":{"songId":song_id}})
        tmp.update({"user_id":update.message.chat.id},{"$set":{"estro":[]}})
        return 0 

def insert_estrofas(update):
  tmp = db.tmp
  tmp.update({"user_id":update.message.chat.id},{"$push":{"estro":int(update.message.text)}})

def insert_general(update):
  tmp = db.tmp
  tmp.update({"user_id":update.message.chat.id},{"$set":{"general":update.message.text}})

def num_estrofas(update):
  tmp = db.tmp
  return len(tmp.find_one({"user_id":update.message.chat.id})["estro"])

def analyzed(update):
  # indica que el usuario analizo la canción cuando el usuario contesto la ultima pregunta.  
  posts = client.users.users
  tmp = client.song.tmp
  song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
  genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
  age = posts.find_one({"user_id":update.message.chat.id})["user_age"]

  genero.update({"_id":song_id},{"$addToSet":{"user_id":update.message.chat.id}})
  genero.update({"_id":song_id},{"$push":{"user_age":{"$each":[int(age)]}}})
  genero.update({"_id":song_id},{"$inc":{"analisis":1}})
  data = genero.find_one({"_id":song_id})["analisis"]
  # si 5 usuarios diferentes terminan de analizar esta cancion la da por validad.
  if data > 4:
    genero.update({"_id":song_id},{"$addToSet":{"valid":1}})

def drop(update):
   #elimina los datos temporales del usuario.
   db.tmp.remove({"user_id":update.message.chat.id})

def reader(update):
   #devuelve la letra de la canción que el usuario escogio análizar.
   tmp = db.tmp
   song_id = tmp.find_one({"user_id":update.message.chat.id})["songId"]
   genero = musical_genre(tmp.find_one({"user_id":update.message.chat.id})["genero"])[0]
   
   data = genero.find_one({"_id":song_id})["Lyrics"]
   
   return data

def sanity(update):
    tmp = db.tmp
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

def letra(data):
   
   letra = {}
   keys = list()
   
   lista = re.findall(r"(?<=])[ê!-?'¡¿\s,a-zA-Z()áéíóúÁÉÍÓÚñÑçã]*",data)
   titulos = re.findall(r"\[[çã!-?'¡¿\s,a-zA-Z()áéíóúÁÉÍÓÚñÑ]+\]",data)
   for i in range(len(lista)):
      if not titulos[i] in letra:
         letra[titulos[i]] = lista[i]
         tag=re.findall(r"(outro|intro|Translation|instrumental|(\[en\]))",titulos[i], flags = re.I)
         if tag == []:
           
           keys.append(titulos[i])
                  
         
   return letra , keys

#crea una base de datos que muestra la letra de las canciónes que estan en la base de datos.
def nombre_tmp(genero):
  allsongs = db.allsongs
  
  for i in range(0, genero.find().count()):
      k = 0
    
      letr , keys = letra(genero.find()[i]["Lyrics"])
      allsongs.insert({"_id":genero.find()[i]["_id"]})
      for j in keys:
         allsongs.update_one({"_id":genero.find()[i]["_id"]},{"$push":{"estrofa":letr[j]}} )
         k+=1

if __name__=='__main__':
 #prueba secilla
  #lyrics('pop',6)
 db.allsongs.drop()
 genero = db.regueton
 nombre_tmp(genero)
 genero = db.pop
 nombre_tmp(genero)
 genero = db.romantica
 nombre_tmp(genero)

