#!/usr/bin/python3

import botconfig as cfg
from telegram import Bot, ParseMode
from classes import dbMonger, iperBimbo


bot = Bot(token=cfg.botToken)
iperBimbo = iperBimbo.iperBimbo(cfg.url, cfg.cookies)
dbM = dbMonger.dbMonger(cfg.mongoDB, cfg.dbName)

myList = iperBimbo.getLista()
for obj in myList:
    message = dbM.insert(obj)
    if message:
        bot.send_message(chat_id=cfg.peppe, text=message, parse_mode=ParseMode.MARKDOWN)  # peppe
        bot.send_message(chat_id=cfg.alice, text=message, parse_mode=ParseMode.MARKDOWN)  # Alice
#listObjects()
