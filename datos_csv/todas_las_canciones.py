#!/bin/python
import config_e
import csv
import json
import logging 
from pymongo import MongoClient
##------------------------------------------------------------------------
## conexión MongoDB
##------------------------------------------------------------------------
try:
  client = MongoClient('localhost',27017)
  #client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("error no se pudo conectar a la base de datos mongoDB")
##------------------------------------------------------------------------
## crea una variable global que accede a la base de datos song.
##------------------------------------------------------------------------
db = client.song

##------------------------------------------------------------------------
## lee la colecion allsongs de MongoDB y la transforma a formato csv.
##------------------------------------------------------------------------

def CSV(name):
          allsongs =db.allsongs
          f = csv.writer(open(name, "w+"))
          f.writerow(["Codigo_cancion","Numero de estrofa","Texo de estrofa"])
                
          total = allsongs.find().count()
          for row in range(0, total):# Number of rows including the death rates 
              
             #x= json.loads(x)
        
             
             for j in range(0,len(allsongs.find()[row]["estrofa"]) ):
               f.writerow([int(allsongs.find()[row]["_id"]),j,allsongs.find()[row]["estrofa"][j]])   
                
                      
             

def main():
  try:
     risk = open('input/allsongs.csv', 'r', encoding="UTF-8").read() #find the file

  except:
      while risk != "input/allsongs.csv":  # if the file cant be found if there is an error
        print("Could not open", risk, "file")
        risk = input("\nPlease try to open file again: ")
  else:
     CSV("output/todas_canciones.csv")     


if __name__ =='__main__':
  main()
       

