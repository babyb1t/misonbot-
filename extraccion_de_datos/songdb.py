#!/usr/bin/python3
# -*- coding: utf-8 -*-
import config_s
from pymongo import MongoClient
import genius_scrapping

##------------------------------------------------------------------------
## conexión MongoDB
##------------------------------------------------------------------------

try:
  client = MongoClient('localhost',27017)
  #client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(variables.user_mongo,variables.passw_mongo))
except Exception as e:
  logging.exception("- Error al conectarse a la BD de MongoDB: ")
## genera la key _id de forma incremental.
def getNextSequence(name,select):
    db = client.song
    if select == 1:
        ret = db.counters.find_and_modify(

            query={"_id":name},
            update={"$inc":{"seq":1}}


        )
    if select == 2:
        ret = db.counters2.find_and_modify(

            query={"_id":name},
            update={"$inc":{"seq":1}}


        )
    if select == 3:
        ret = db.counters3.find_and_modify(

            query={"_id":name},
            update={"$inc":{"seq":1}}


        )
    return ret["seq"]


#crea la estructura de la base de datos.
def dbs(select,song_name,artista,lyrics):
    db = client.song
    if select == 1:
        genero = db.regueton
        gen = 'regueton'
    if select == 2:
        genero = db.pop
        gen = 'pop'
    if select == 3:
        genero = db.romantica
        gen = 'romantica'

    if lyrics != None:
        genero.insert({"_id": getNextSequence("songId",select),
                  "Name_song":song_name,
                  "Genero":gen,
                  "Artista":artista,
                  "user_id":[],
                  "user_age":[],
                  "analisis":0,
                  "valid":0,
                  "Lyrics":lyrics
                   })




if __name__ == '__main__':
    #(song_name = "q=Despacito", artista = "Luis Fonsi") formato
    regueton = [("Échame La Culpa","Luis Fonsi & Demi Lovato"),("Perro Fiel","Shakira"), ("Criminal","Natti Natasha"),
                 ("Corazón","Maluma"), ("Mi Gente (feat. Beyoncé)","J Balvin & Willy William"),("Mayores","Becky G"),
                 ("Déjate Llevar","Juan Magán"),("Despacito","Luis Fonsi"),("Súbeme La Radio","Enrique Iglesias")]
    pop = [("Perfect Duet" ,"Ed Sheeran & Beyonce"), ("Havana","Camila Cabello"), ("What Lovers Do","Maroon 5"),
           ("Wolves","Selena Gomez & Marshmello"), ("How Long","Charlie Puth"),("New Rules","Dua Lipa"),
           ("Dusk Till Dawn","ZAYN"), ("Tip Toe","Jason Derulo"), ("Anywhere","Rita Ora"),("Guerrera","C. Tangana"),
           ("Guerrera","C. Tangana"),("El Patio","Pablo López"),("No Vaya A Ser","Pablo Alborán"),("Saturno","Pablo Alborán"),
           ("Invisible","Malu"),("24K Magic","Bruno Mars"),("Rockabye","Clean Bandit"),("Don't Wanna Know","Maroon 5"),
           ("Lost on You","LP"),("Come","Jain"),("Perfect Strangers","Jonas Blue"),("Cómo Te Atreves","Morat"),("Espectacular","Fangoria")]
    romantica = [("Deja Que Te Bese","Alejandro Sanz"),("Espectacular","Fangoria"),("Yo Contigo, Tú Conmigo (The Gong Gong Song)","Morat"),            
                ("Míranos","Álex Ubago")]
   

  

    for song_name, artista in regueton:
        dbs(1,song_name,artista,genius_scrapping.lyrics(song_name,artista))
    for song_name, artista in pop:
        dbs(2,song_name,artista,genius_scrapping.lyrics(song_name,artista))
    for song_name, artista in romantica:
       dbs(3,song_name,artista,genius_scrapping.lyrics(song_name,artista))
