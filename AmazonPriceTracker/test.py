#!/usr/bin/env python3
import botconfig as cfg
import requests, re
from bs4 import BeautifulSoup
from classes import dbMonger
from csv import reader
from telegram import Bot, ParseMode

def getPrice(URL):
    page = requests.get(URL, headers={"User-Agent": ''})
    soup0 = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup0.prettify(), "html.parser")

    productPrice = soup.find(id="priceblock_ourprice").get_text()
    priceRex = re.search('(\d+,\d+).+€', productPrice)
    if priceRex:
        return priceRex.group(1)
    else:
        retun

bot = Bot(token=cfg.botToken)
dbM = dbMonger.dbMonger(cfg.mongoDB, cfg.dbName, cfg.trackerCollection)

# open file in read mode
with open('prices.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # 0 title
        # 1 URL
        message = None
        currentPrice = getPrice(row[1])
        oldObject = dbM.search({'name' : row[0] })
        #print(oldObject)
        if not oldObject:
            dbM.insert({'name': row[0],
                        'price': currentPrice,
                        'oldPrice': currentPrice})
            message = "%s\nE' stato inserito nel database, attualmente il suo prezzo e' %s €" % (row[0], currentPrice)
        else:
            newObject = dict(oldObject)
            newObject['price'] = currentPrice
            if currentPrice > oldObject['price']:
                #print('Il Prezzo e salito')
                message = "%s\nIl prezzo e' salito!\nAdesso costa %s €" % (row[0], currentPrice)
            elif currentPrice < oldObject['price']:
                #print('Il Prezzo e sceso')
                message = "%s\nIl prezzo e' sceso!\nAdesso costa %s €" % (row[0], currentPrice)
            else:
                next
                #print('Prezzo uguale')

            dbM.update(oldObject, newObject)

    if message:
        bot.send_message(chat_id=cfg.peppe, text=message, parse_mode=ParseMode.MARKDOWN)  # peppe