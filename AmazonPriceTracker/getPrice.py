import requests, re
from bs4 import BeautifulSoup

URL = 'https://www.amazon.it/Interruttore-Piccolo-Telecomando-Supporto-Funziona/dp/B07V615TZ8/ref=sr_1_6?__mk_it_IT=ÅMÅŽÕÑ&dchild=1&keywords=sonoff&qid=1610139170&sr=8-6'

page = requests.get(URL, headers={"User-Agent": ''})
soup0 = BeautifulSoup(page.content, "html.parser")
soup = BeautifulSoup(soup0.prettify(), "html.parser")

productPrice = soup.find(id="priceblock_ourprice").get_text()
priceRex = re.search('(\d+,\d+.+€)', productPrice)
if priceRex:
    productPrice = priceRex.group(1)

print(productPrice)