#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import botconfig as cfg
from classes import dbMonger, iperBimbo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('\n'.join(cfg.helpRows))

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def lista(update, context):
    cursor = dbM.listAll()
    toPrint = ""
    for ogg in cursor:
        if ogg['promised'].lower() == 'acquistato' or ogg['promised'].lower() == 'prenotato':
            toPrint = "%s\n%s %s - %s (%s) - %s" % (toPrint, cfg.emoticons[ogg['promised'].lower()], ogg['name'], ogg['promised'], ogg['buyer'], ogg['price'])
        else:
            toPrint = "%s\n%s - %s" % (toPrint, ogg['name'], ogg['price'])
    update.message.reply_text(toPrint)

def comprati(update, context):
    cursor = dbM.listAll()
    toPrint = ""
    for ogg in cursor:
        if ogg['promised'].lower() == 'acquistato':
            toPrint = "%s\n%s - %s (%s) - %s" % (toPrint, ogg['name'], ogg['promised'], ogg['buyer'], ogg['price'])
    update.message.reply_text(toPrint)

def prenotati(update, context):
    cursor = dbM.listAll()
    toPrint = ""
    for ogg in cursor:
        if ogg['promised'].lower() == 'prenotato':
            toPrint = "%s\n%s - %s (%s) - %s" % (toPrint, ogg['name'], ogg['promised'], ogg['buyer'], ogg['price'])
    update.message.reply_text(toPrint)

def updateDb(update, context):
    myList = iperBimbo.getLista()
    for obj in myList:
        message = dbM.insert(obj)
        if message:
            update.message.reply_text(message)
    update.message.reply_text("%s DB Aggiornato" % u'\U0001F44C')

def test(update, context):
    update.message.reply_text("Acquistato %s \nPrenotato %s" % (cfg.emoticons['acquistato'], cfg.emoticons['prenotato']))

iperBimbo = iperBimbo.iperBimbo(cfg.url, cfg.cookies)
dbM = dbMonger.dbMonger(cfg.mongoDB, cfg.dbName)

updater = Updater(cfg.botToken, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", help))
dp.add_handler(CommandHandler("lista", lista))
dp.add_handler(CommandHandler("comprati", comprati))
dp.add_handler(CommandHandler("prenotati", prenotati))
dp.add_handler(CommandHandler("aggiorna", updateDb))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("test", test))


# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()