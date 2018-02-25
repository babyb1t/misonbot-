#!/usr/bin/python3

import re
import sys
import variables
import logging
from pymongo import MongoClient
from random import randint
try:
  client = MongoClient('localhost',27017)
  #client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("- Error al conectarse a la BD de MongoDB: ")  

db = client.song
allsongs = db.allsongs
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
def song_insert(genero):
    
  for i in range(0, genero.find().count()):
      k = 0
      try:

        letr , keys = letra(genero.find()[i]["Lyrics"])

      except Exception as e:

        print("  ",time.strftime("%c"),"- Error letra no encontrada: ", type(e), e)

      allsongs.insert({"_id":genero.find()[i]["_id"]})
      for j in keys:
         allsongs.update_one({"_id":genero.find()[i]["_id"]},{"$push":{"estrofa":letr[j]}} )
         k+=1

if __name__=='__main__':
 
 allsongs.drop()
 genero = db.regueton
 song_insert(genero)
 genero = db.pop
 song_insert(genero)
 genero = db.romantica
 song_insert(genero)
