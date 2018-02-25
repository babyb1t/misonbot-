#!/bin/python

import csv
import json
import logging 
from pymongo import MongoClient
try:
  client = MongoClient('localhost',27017)
except Exception as e:
  logging.exception("error no se pudo conectar a la base de datos mongoDB")
db = client.song

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
     risk = open('datos_csv/input/allsongs.csv', 'r', encoding="UTF-8").read() #find the file

  except:
      while risk != "datos_csv/input/allsongs.csv":  # if the file cant be found if there is an error
        print("Could not open", risk, "file")
        risk = input("\nPlease try to open file again: ")
  else:
     CSV("datos_csv/output/todas_canciones.csv")     


if __name__ =='__main__':
  main()
       

