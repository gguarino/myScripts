import requests, re
from bs4 import BeautifulSoup
class iperBimbo:

    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    def getLista(self, reset=False):
        lista = []
        response = requests.get(self.url, cookies=self.cookies)

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all('div', {"class": "wishlist-item"}):
            articolo = {}
            articolo['promised'] = articolo['buyer'] = 'None'
            articolo['name'] = link.h3.string
            priceTag = link.find('div', attrs={'class': 'wishlist-price'})
            if priceTag:
                articolo['price'] = priceTag.string

            promiseTag = link.find('span', attrs={'class': 'wishlist-promised'})
            if promiseTag and not reset:
                promisRex = re.search("([A-Za-z]+) da (.*)!", promiseTag.string)
                if promisRex:
                    articolo['promised'] = promisRex.group(1)
                    articolo['buyer'] = promisRex.group(2)

            lista.append(articolo)

        return lista

    def getListaTest(self, reset=False):

        lista = []
        with open('/home/pinux/Documents/myPythonScripts/listaNascitaBot/output.html', 'r') as f:
            response = f.read()

        soup = BeautifulSoup(response, "html.parser")

        for link in soup.find_all('div', {"class": "wishlist-item"}):
            articolo = {}
            articolo['promised'] = articolo['buyer'] = 'None'
            articolo['name'] = link.h3.string
            priceTag = link.find('div', attrs={'class': 'wishlist-price'})
            if priceTag:
                articolo['price'] = priceTag.string

            promiseTag = link.find('span', attrs={'class': 'wishlist-promised'})
            if promiseTag and not reset:
                promisRex = re.search("([A-Za-z]+) da (.*)!", promiseTag.string)
                if promisRex:
                    articolo['promised'] = promisRex.group(1)
                    articolo['buyer'] = promisRex.group(2)

            lista.append(articolo)

        return lista