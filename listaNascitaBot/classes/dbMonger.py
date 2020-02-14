from pymongo import MongoClient
import datetime


class dbMonger:

    def __init__(self, address, dbName):
        self.client = MongoClient()
        self.client = MongoClient(address)
        self.mydatabase = self.client[dbName]

    def insert(self, oggetto):
        searchObj = self.mydatabase.jacopino.find_one({
            'name': oggetto['name']
        })
        if searchObj is not None:
            changed = False
            # per la modifica prendi l'oggetto e confrontalo con quello che hai
            for key in searchObj:  # s chiave, searchObj[s] valore
                if key not in ['_id', 'lastUpdate','price']:
                    if searchObj[key] != oggetto[key]:
                        # print("%s is different for %s" % (oggetto[key], oggetto['name']))
                        changed = True
                        # print(searchObj[key])
            if changed:
                # print('Modifico il campo')
                oggetto['lastUpdate'] = datetime.datetime.now().strftime("%s")
                self.mydatabase.jacopino.update_one({"_id": searchObj["_id"]}, {"$set": oggetto})  # Update
                # MANDA IL MESSAGGIO AL BOT
                return ("L'oggetto %s e' stato %s da %s" % (
                oggetto['name'], oggetto['promised'].lower(), oggetto['buyer']))
        else:
            oggetto['lastUpdate'] = datetime.datetime.now().strftime("%s")
            rec = self.mydatabase.jacopino.insert(oggetto)  # Insert in mongo
        # return(oggetto['name'])

    def listAll(self, search={}):
        return self.mydatabase.jacopino.find(search)
