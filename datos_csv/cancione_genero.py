#!/bin/env python
import csv
import re
import variables
from pymongo import MongoClient
from pathlib import Path
try:
  client = MongoClient('localhost',27017)
  #client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("- Error no se pudo conectar a la base de datos")

db = client.song
def read_and_write(namer,namew):

  with open(namer) as fr:
    reader = csv.reader(fr, delimiter=',')
    
    fw = csv.writer(open(namew, "w+"))
    fw.writerow(["Codigo_cancion","Name_song","Genero","Artista","user_id","user_age","analisis","valid"])
    i = 0
    for row in reader:
      
      if i > 0:
        row[5] = re.sub(r'[\[\]]','',row[5])
        row[5] = row[5].split(',')
        row[4] = re.sub(r'[\[\]]','',row[4])
        row[4] = row[4].split(',')
        if len(row[4]) > 1:
        
          for i in range(0, len(row[4])):
          
            fw.writerow([row[0],row[1],row[2],row[3],int(row[4][i]),int(row[5][i]),row[6],row[7]]) 
            CSV(int(row[0]),int(row[4][i]))
        if len(row[4])==1:
            if row[5][0].isdigit(): 
                fw.writerow([row[0],row[1],row[2],row[3],int(row[4][0]),int(row[5][0]),row[6],row[7]])
                CSV(int(row[0]),int(row[4][0]))
            else:     
                fw.writerow([row[0],row[1],row[2],row[3],0,0,row[6],row[7]])
       

      i += 1

def CSV(codigo_cancion,user_id):
      
          allsongs =db.allsongs
          my_file = Path("./datos_csv/canciones_analisadas.csv")
          if my_file.is_file():
            print(my_file.is_file())
            f = csv.writer(open("./datos_csv/canciones_analisadas.csv", "a"))
            for j in range(0,len(allsongs.find_one({'_id':codigo_cancion})["estrofa"]) ):
              f.writerow([user_id,codigo_cancion,j,allsongs.find_one({'_id':codigo_cancion})["estrofa"][j]])
          
          else:
            f = csv.writer(open("./datos_csv/canciones_analisadas.csv", "w"))
            f.writerow(["user_id","Codigo_cancion","Numero de estrofa","Texo de estrofa"])


   
def main():
  read_and_write("./datos_csv/input/raw_pop.csv","./datos_csv/output/pop.csv")
  read_and_write("./datos_csv/input/raw_regueton.csv","./datos_csv/output/regueton.csv")
  read_and_write("./datos_csv/input/raw_romantica.csv","./datos_csv/output/romantica.csv")
      

if __name__=='__main__':
  main()
