# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from subprocess import call
import sqlite3 as lite
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, filename='bot.log')

updater = Updater('token')


def read_db(id):
    id_array = []
    con = None
    try:
        con = lite.connect('apps.db')
        
        cur = con.cursor()                
        adminID = "id"+str(id)

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = cur.fetchall()
        if data == []:
            print "no users there!"
        else:
            print("users: %s"%data)
    
        cur.execute("SELECT * FROM %s;"%adminID)
        rows=cur.fetchall()
        for row in rows:
            item = [row[1],row[2]]
            id_array.append(item)

    except lite.Error, e:
        
        print "Error %s:" % e.args[0]
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()

    return id_array

def menu(bot, update):
    id_array = []
    con = None
    try:
        con = lite.connect('apps.db')
        
        cur = con.cursor()                
        adminID = "id"+str(update.message.from_user.id)

        data= "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"%adminID
        if not cur.execute(data).fetchone():
            print("FUCK! ID ", update.message.from_user.id, "is not in our db.")
            update.message.reply_text("You're not authorized to do this. Fuck off!")
            return
        else:
            print("yea! ID ", update.message.from_user.id, "is in our db. Continue working!")
        
    except lite.Error, e:
        
        print "Error %s:" % e.args[0]
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()


    try:
        db=read_db(update.message.from_user.id)
        keyboard = []
        for item in db:
            keyboard.append([KeyboardButton(item[0])])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True ,one_time_keyboard = True)
        msg = bot.send_message(chat_id=update.message.chat_id, text="Menu", reply_markup=reply_markup)
        updater.dispatcher.add_handler(MessageHandler(Filters.text, name))
    except Exception as e:
        print("error:", str(e))


def name(bot, update):
    db=read_db(update.message.from_user.id)

    text = update.message.text
    for item in db:
        if text == item[0]:
            update.message.reply_text('trying to start %s'%item[0], call(["open", "-a", item[1]]))


def hello(bot, update):
    update.message.reply_text('Yo, {}!'.format(update.message.from_user.username))
    
def who(bot, update):
    update.message.reply_text('Your id is {}'.format(update.message.from_user.id))



updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('who', who))

    

updater.start_polling()
updater.idle()
