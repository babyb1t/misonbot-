#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import read_db
import chat
import variables
from telegram import  (ReplyKeyboardMarkup, ReplyKeyboardRemove, User, Bot,InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters,RegexHandler,CallbackQueryHandler)




EDAD, SEXO ,CANCIONES ,ESTEROTIPO, GENRE, AWNSER1, ROLES, AWNSER2, PODER, AWNSER3, CUERPO, AWNSER4,GENERAL, AWNSER5, END1 = range(15)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def teclado(select):
  bol = False
  if select == 1:
    keyboard = [['Chico','Chica']]

  if select == 2:
    keyboard = [['Sí','No']]
    bol = True
  if select == 3:
    keyboard = [['1','2','3','4','5'],['6','7','8','9','10'],['ninguna','\U0001f51a']]
  if select ==4:
    keyboard = [["pop","reguetón"],["romántica"]]

  if select == 5:
    keyboard = [['1','2','3','4','5'],['6','7','8','9','10']]
  if select == 6:
    keyboard = [['otra canción', 'continuar']]

  reply_markup = ReplyKeyboardMarkup(keyboard , resize_keyboard = True, one_time_keyboard= bol )
  return reply_markup



def check_number(update):
  #compara el numero introducido en el taclado con la cantidad de estrofas
   
  keys = read_db.lyrics(update)[1]
  
  if int(update.message.text) <= len(keys):
      read_db.insert_estrofas(update)
  else:
      update.message.reply_text('Solo hay %d estrofas' % ( len(keys) ))
 
def mostrar_cancion(bot,update):
    #muestra la cancion que esta ciendo analizada por el usuario
    if read_db.sanity(update):
      # verifica si el usuario ya ha elegido alguna canción y la muestra en la conversación.
      letras , keys = read_db.lyrics(update)
      bot.sendMessage(chat_id = update.message.chat_id, text = 'Esta es la letra de la canción:\n Nombre: %s'%(read_db.song_name(update)))
      bot.sendMessage(chat_id = update.message.chat_id, text = '--INICIO CANCIÓN--')    
      for i in range(len(keys)):
          bot.sendMessage(chat_id = update.message.chat_id, text = "Estrofa: %d\n%s" %(i + 1, letras[keys[i]]))
      bot.sendMessage(chat_id = update.message.chat_id, text = '--FIN CANCIÓN--')   
    else:
      bot.sendMessage(chat_id = update.message.chat_id, text = 'No tienes ninguna canción para mostrar')

def conceptos(bot, update):
  #muestra los conceptos de misoginia
  f = open('conceptos.txt','r')
  concep = f.read()
  bot.sendMessage(chat_id = update.message.chat.id, text= concep)
  f.close()
  f = open('conceptos1.txt','r')
  concep = f.read()
  bot.sendMessage(chat_id = update.message.chat.id, text= concep)
  f.close()

def acerca_de(bot,update):
  bot.sendMessage(chat_id = update.message.chat_id, text = "#MúsicaMisòginaOFF és un bot que analitza lletres de cançons per detectar "
                                                           "el masclisme en la música. Desenvolupat per l'IES de Malilla, amb la "
                                                           "col·laboració de la Ajuntament de València - UPV, "
                                                           "la UV i Las Naves'")

def start(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Hola {}. gracias por participar. Para interactuar conmigo puedes usar estos comandos:'.format(update.message.from_user.first_name))
    bot.sendMessage(chat_id = update.message.chat_id, text = 
                   '/acerca_de Entidades y personas involucradas.\n'
                   '/analizar Para analizar una nueva cancion.\n'
                   '/ayuda Da una descripcion del funcionamiento del bot.\n'
                   '/conceptos Ofrece una explicación para cada uno de los conceptos.\n' 
                   '/cancel Cancelar el análisis.\n'
                   '/cancion Muestra la letra de la canción.\n'
                   'Puedes acceder a estos comandos en cualquier momento pulsando la barra /.' 
                   )
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Para comenzar pulsa /analizar.')




def analizar(bot, update):
     
   if chat.user_exists(update):
       #verifica si a usado el chat bo antes
       bot.sendMessage( chat_id=update.message.chat_id , text = "Encantado {} que quieras continuar.".format(update.message.from_user.first_name))

       read_db.drop(update)
       bot.sendMessage( chat_id=update.message.chat_id, text="Elige el género musical que quieres analizar."
                                              , reply_markup=teclado(4))
       return CANCIONES
   else:
       #si no realiza la primera entrada.
       bot.sendMessage(chat_id=update.message.chat_id, text="Un par de preguntas rápidas para conocerte."
                                                  " ¿Me dices tu edad, por favor?")
       return SEXO


def sexo(bot, update):
  

    if update.message.text.isdigit() and  int(update.message.text) > 10 and int(update.message.text) < 70:
        chat.user_age(update)
        #inserta la edad del ususario.
        bot.sendMessage(chat_id=update.message.chat_id, text = '¿Eres chico o chica?', reply_markup= teclado(1))
        return GENRE 
    if update.message.text.isdigit() and int(update.message.text) <= 10:
        bot.sendMessage(chat_id=update.message.chat_id, text = '¿No crees que eres algo joven?')
    if update.message.text.isdigit() and  int(update.message.text) > 70:
        bot.sendMessage(chat_id=update.message.chat_id, text = '¿No crees que eres algo mayor?')
        return SEXO

def genre(bot,update):
   
     if update.message.text == 'Chico' or  update.message.text == 'Chica':
       chat.user_sexo(update)
       #inserta el sexo del usuario.
       bot.sendMessage(chat_id = update.message.chat.id, text='Elige el género musical que quieres analizar.'
                                                    ,reply_markup = teclado(4))
       
       return CANCIONES
     else:
       bot.sendMessage(chat_id = update.message.chat.id, text='Oops! usa el teclado emergente.')


def canciones(bot, update ):
    
    if read_db.new_song(update):
    #selecciona una cancion nueva
        bot.sendMessage(chat_id = update.message.chat_id, text = '!!!Disculpad, tenemos que ampliar la base de datos, prueba con otro género.',
                        reply_markup =ReplyKeyboardRemove() )
        
        return ConversationHandler.END
    #extrae la letra de la cancion de la base de dato
    letras , keys = read_db.lyrics(update)

    bot.sendMessage(chat_id = update.message.chat_id, text = 'Esta es la letra de la canción:\n Nombre: %s'%(read_db.song_name(update)))
    bot.sendMessage(chat_id = update.message.chat_id, text = '--INICIO CANCIÓN--')
    for i in range(len(keys)):
        bot.sendMessage(chat_id = update.message.chat_id, text = "Estrofa: %d\n%s" %(i + 1, letras[keys[i]]))

    bot.sendMessage(chat_id = update.message.chat_id, text = '--FIN CANCIÓN--')
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Ahora, voy a hacerte una serie de preguntas'
                    ' relacionadas con la letra de la canción. Para responderlas utiliza el teclado emergente '
                    'que he diseñado. Si no te interesa está canción pulsa otra_cancion para analizar una canción diferente.\n'
                    'O pulsa continuar para seguir con esta canción.'
                    , reply_markup = teclado(6))
    return ESTEROTIPO

def estereotipo(bot, update):
  if update.message.text == 'continuar': 
    bot.sendMessage( chat_id = update.message.chat_id, text = 'Comencemos...'
                    '\nPulsa el número de  aquellas estrofas que contienen estereotipos (creencias que suponen '
                    'generalizaciones sobre lo que “debe ser” una mujer y/o un hombre).'
                    ' Presiona \U0001f51a para terminar y pasar a la siguiente pregunta.', reply_markup = teclado(3))

    chat.base(update, read_db.song_name(update))
    #inserta la estructura de los datos en en la base de datos mongo.    
    return AWNSER1
  else:
    bot.sendMessage( chat_id = update.message.chat_id, text ='Elige el género musical que quieres analizar.'
                                                             , reply_markup = teclado(4))
    return CANCIONES

def awnser1(bot,update):
   
    if  update.message.text == 'ninguna':
        bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Pulsa el número de aquellas estrofas que contienen una diferencia de roles: papeles, tareas,'
                       ' normas que debe asumir la mujer y el hombre en sociedad. Por ej. Se espera que las mujeres'
                       ' cuiden de los familiares enfermos.', reply_markup = teclado(3))
        chat.estereotipo(update, read_db.song_name(update))
        #guarda la respuesta estereotipo
        return AWNSER2
    if update.message.text.isdigit():
       check_number(update)
       
       return AWNSER1
    if update.message.text == '\U0001f51a' and read_db.num_estrofas(update) > 0:
        bot.sendMessage(chat_id = update.message.chat_id,
                        text = 'En una escala de 1 a 10, siendo 1 el nivel más bajo y 10 el más alto, '
                        '¿en qué medida dichos estereotipos degradan a la mujer o la sitúan en una posición'
                        ' “inferior-débil” frente al hombre?', reply_markup = teclado(5) )
        

        return ROLES

def roles(bot,update):
    if update.message.text.isdigit():
       
       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Pulsa el número de aquellas estrofas que contienen una diferencia de roles: papeles, tareas, '
                       'normas que debe asumir la mujer y el hombre en sociedad. Por ej. se espera que las mujeres'
                       ' cuiden de los familiares enfermos.', reply_markup = teclado(3) )
       chat.estereotipo(update, read_db.song_name(update))
       #guarda respuesta estereotipo.
       return AWNSER2
    else:
        update.message.reply_text('Tiene que ser un número del 1 al 10')
        return ROLES


def awnser2(bot,update):
    
    if  update.message.text == 'ninguna':
       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Pulsa el número de aquellas estrofas que plantean posiciones de desigualdad, otorgando '
                       'más poder a los hombres que a las mujeres.', reply_markup = teclado(3) )

       chat.roles(update,read_db.song_name(update) )
       #guarda respuesta roles en mongodb.
       return AWNSER3
    if update.message.text.isdigit():
      check_number(update)
      
      return AWNSER2
    if update.message.text == '\U0001f51a' and read_db.num_estrofas(update) > 0:
        bot.sendMessage(chat_id = update.message.chat_id,
                        text ='En una escala de 1 a 10, siendo 1 el nivel más bajo y 10 el más alto, '
                        '¿en qué medida los roles asignados a las mujeres poseen menos reconocimiento '
                        'social que los de los hombres?', reply_markup = teclado(5) ) 
        

        return PODER

def poder(bot,update):
    if update.message.text.isdigit():
       
       bot.sendMessage(chat_id = update.message.chat_id,
                       text ='Pulsa el número aquellas estrofas que plantean posiciones de desigualdad, otorgando '
                       'más poder a los hombres que a las mujeres.', reply_markup = teclado(3) )
       chat.roles(update, read_db.song_name(update))
       
       return AWNSER3
    else:
        update.message.reply_text('Tiene que ser un número del 1 al 10')
        return PODER


def awnser3(bot,update):
    
    if  update.message.text == 'ninguna':
       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Pulsa el número de aquellas estrofas que se refieren al cuerpo de las mujeres.',
                       reply_markup = teclado(3))
       chat.poder(update, read_db.song_name(update))
       return AWNSER4
    if update.message.text.isdigit():
      check_number(update)
      return AWNSER3
    if update.message.text == '\U0001f51a' and read_db.num_estrofas(update) > 0:
        bot.sendMessage(chat_id = update.message.chat_id,
                        text = 'En una escala de 1 a 10, siendo 1 el nivel más bajo y 10 el más alto, '
                               '¿en qué medida se plantea una relación de dominación?', reply_markup = teclado(5) )

       
        return CUERPO

def cuerpo(bot,update):
    if update.message.text.isdigit():
       
       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Pulsa el número aquellas estrofas que se refieren al cuerpo de las mujeres.',
                       reply_markup = teclado(3) )
       chat.poder(update, read_db.song_name(update))
       return AWNSER4
    else:
        update.message.reply_text('Tiene que ser un número del 1 al 10')
        return CUERPO


def awnser4(bot,update):
    
    if  update.message.text == 'ninguna':

       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Por ultimo ¿consideras sexista esta canción?', reply_markup=teclado(2))
       chat.cuerpo(update, read_db.song_name( update))
       return AWNSER5
    if update.message.text.isdigit():
       check_number(update)
       
       return AWNSER4
    if update.message.text == '\U0001f51a' and read_db.num_estrofas(update) > 0:
        bot.sendMessage(chat_id = update.message.chat_id,
                        text ='En una escala de 1 a 10, siendo 1 el nivel más bajo y 10 el más alto, '
                        '¿en qué medida se les otorga un valor de “objeto sexual”?'
                        ,reply_markup = teclado(5))
      
        return GENERAL

def general(bot,update):
    if update.message.text.isdigit():
       
       bot.sendMessage(chat_id = update.message.chat_id,
                       text = 'Por ultimo ¿consideras sexista esta canción?', reply_markup=teclado(2))
       chat.cuerpo(update, read_db.song_name(update))
       
       return AWNSER5
    else:
        update.message.reply_text('Tiene que ser un número del 1 al 10')
        return GENERAL




def awnser5(bot,update):
    
    if  update.message.text == 'No' or update.message.text == 'no':
       bot.sendMessage(chat_id=update.message.chat_id, text = '¡Genial! Hemos completado el análisis de esta canción.'
                      ' Si quieres analizar otra canción teclea el comando /analizar',reply_markup =ReplyKeyboardRemove())
       read_db.analyzed(update)
       chat.general(update, read_db.song_name(update))
       
       return ConversationHandler.END

    if update.message.text == 'Sí' or update.message.text == 'Si' or update.message.text == 'sí' or update.message.text == 'Sí':
        bot.sendMessage(chat_id = update.message.chat_id,
                        text = 'En una escala de 1 a 10, siendo 1 el nivel más bajo y 10 el más alto, '
                                '¿En qué grado consideras esta canción sexista?',reply_markup=teclado(5))

        aux = update.message.text
        return END1



def end (bot, update):
  
  bot.sendMessage(chat_id=update.message.chat_id, text = '¡Genial! Hemos completado el análisis de esta canción.'
                    ' Si quieres analizar otra canción\n teclea el comando /analizar ', reply_markup =ReplyKeyboardRemove())
  chat.general(update, read_db.song_name(update))
  read_db.analyzed(update)
  #da la cancion por análizada.
  read_db.drop(update)
  #elimina documento temporal al finalizar el análisis.
  #cierra conversación.
  return ConversationHandler.END

#funcion que guarda errores del bot.
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def cancel(bot,update):

  read_db.drop(update)
  #elimina documento temporal al cancelar el análisis.
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  bot.sendMessage(chat_id=update.message.chat_id, text = 'Hasta otra {}'.format(user.first_name)
                    , reply_markup =ReplyKeyboardRemove())
  return ConversationHandler.END

def ayuda(bot,update):

  update.message.reply_text('Mison es un bot de encuesta que consiste en analizar el contenido machista en una canción, '
                            'para empezar (presiona el comando\n/analizar).'
                            ' Luego tendrás que contestar 10 preguntas donde se te pedirá que ingreses las estrofas que  tengan contenido'
                            ' machista y su grado de ofensa, en relación a los siguientes conceptos: estereotipo, roles de género, '
                            ' figura femenina y sexismo.\n\n'
                            'Cada estrofa tendrá un número en la parte superior, ese número será el que debes'
                            ' ingresar para indicarnos cuales estrofas te parecieron machistas y por último '
                            'para indicar el grado de ofensa debes calificarlo con un valor del 1 al 10, ' 
                            'siendo 1 el nivel más bajo y 10 el más alto.' ,
                            reply_markup=ReplyKeyboardRemove())


def main():

  updater = Updater(variables.Token_bot)


  conv_handler = ConversationHandler(
        entry_points=[CommandHandler('analizar', analizar)],

        states={

            
            SEXO:[RegexHandler('^([0-9][0-9]?)$', sexo)],
            GENRE:[MessageHandler(Filters.text, genre)],
            CANCIONES:[RegexHandler('^(pop|romántica|reguetón)$', canciones)],
            ESTEROTIPO:[RegexHandler('^(otra canción|continuar)$', estereotipo)],
            AWNSER1:[RegexHandler('^([0-9][0-9]?|ninguna|\U0001f51a)$', awnser1)],
            ROLES: [MessageHandler(Filters.text, roles)],
            AWNSER2:[RegexHandler('^([0-9][0-9]?|ninguna|\U0001f51a)$', awnser2)],
            PODER: [MessageHandler(Filters.text, poder)],
            AWNSER3:[RegexHandler('^([0-9][0-9]?|ninguna|\U0001f51a)$', awnser3)],
            CUERPO: [MessageHandler(Filters.text, cuerpo)],
            AWNSER4:[RegexHandler('^([0-9][0-9]?|ninguna|\U0001f51a)$', awnser4)],
            GENERAL: [MessageHandler(Filters.text, general)],
            AWNSER5:[RegexHandler('^(Si|No|si|no|sí|Sí)$', awnser5)],
            END1: [RegexHandler('^([0-9][0-9]?|\U0001f51a)$', end)]

        },

        fallbacks=[CommandHandler('cancel', cancel)], 
        allow_reentry=True
  )
  updater.dispatcher.add_error_handler(error)
  updater.dispatcher.add_handler(CommandHandler('start',start))
  updater.dispatcher.add_handler(conv_handler)
  updater.dispatcher.add_handler(CommandHandler('cancion',mostrar_cancion))
  updater.dispatcher.add_handler(CommandHandler('conceptos',conceptos))
  updater.dispatcher.add_handler(CommandHandler('ayuda',ayuda))
  updater.dispatcher.add_handler(CommandHandler('acerca_de',acerca_de))
  updater.start_polling()
  #updater.start_webhook(listen='0.0.0.0',
  #                    port=8443,
  #                    url_path=variables.Token_bot,
  #                    key='private.key',
  #                    cert='cert.pem',
  #                    webhook_url='{}:8443/{}'.format(variables.url, variables.Token_bot))

  updater.idle()


if __name__=='__main__':
  main()
