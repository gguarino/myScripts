    #!/usr/bin/python3

import botconfig as cfg
from classes import dbMonger, iperBimbo

iperBimbo = iperBimbo.iperBimbo(cfg.url, cfg.cookies)
dbM = dbMonger.dbMonger(cfg.mongoDB, cfg.dbName)

myList = iperBimbo.getLista(True)
for obj in myList:
    dbM.insert(obj)