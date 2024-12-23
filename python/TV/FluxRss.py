from bs4 import BeautifulSoup
import requests
import random
import time
import threading
from collections import Counter

class FluxRss :
    def __init__(self):
        self.titres = []
        self.mot1 = ""

    def maj(self):
        threadRss = threading.Thread(target=self.getRss)
        threadRss.start()

    def getRss(self):
        urls=[]
        urls.append("https://www.lemonde.fr/rss/une.xml")
        urls.append("https://www.humanite.fr/feed")
        urls.append("https://www.liberation.fr/arc/outboundfeeds/rss-all/?outputType=xml")
        urls.append("https://www.valeursactuelles.com/feed?post_type=post")
        urls.append("https://www.lefigaro.fr/rss/figaro_actualites.xml")
        urls.append("https://services.lesechos.fr/rss/les-echos-monde.xml")
        urls.append("https://www.la-croix.com/RSS/UNIVERS")
        urls.append("https://feeds.leparisien.fr/leparisien/rss")
        urls.append("https://www.courrierinternational.com/feed/rubrique/france/rss.xml")
        urls.append("https://www.lexpress.fr/arc/outboundfeeds/rss/alaune.xml")
        titresTemporaires = []
        for url in urls:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content,features='xml')
            items = soup.find_all('item')
            for item in items:
                texte = item.title.get_text(strip=True)
                if (not texte.startswith("Météo")) : # sur le Parisien plein de Météo à virer
                    titresTemporaires.append(texte)
        self.titres = titresTemporaires
        self.majMot1()
        print("")
        print("Maj des RSS effectuée")
        print("")


    def getTitreRandom(self):
        if(len(self.titres)>0):
            n = random.randrange(len(self.titres))
            return self.titres[n]
        else :
            return ""

    def majMot1(self):
        texteBrut = ""
        if(len(self.titres) == 0) : return ""
        for t in self.titres:
            texteBrut+=t
            texteBrut+=" "
        texteBrut=texteBrut.replace(',',' ')
        texteBrut=texteBrut.replace(';',' ')
        texteBrut=texteBrut.replace(':',' ')
        texteBrut=texteBrut.replace('’',' ')
        texteBrut=texteBrut.replace('«',' ').replace('»',' ')
        texteBrut=texteBrut.replace('…',' ')
        texteBrut=texteBrut.replace('\"',' ')
        texteBrut=texteBrut.replace('\n',' ')
        texteBrut=texteBrut.replace('!',' ')
        texteBrut=texteBrut.replace(u'\xa0', ' ')
        texteBrut = texteBrut.strip()
        ''.join(i for i in texteBrut if not i.isdigit())
        motsBruts = texteBrut.split(' ')
        mots=[]
        motsInterdits=['avec','avant','nouveau','sont','pour','dans','plus','moins','Météo','après','contre','face','encore','sait','vous','cette','faire','entre','premier','toujours','euros','nous','sera','vers','prix','sous','fait','enfin','être','sans','aussi','leur','leurs','bien','jour','comme','près']
        for m in motsBruts :
            if(len(m)>3):
                isInterdit = False
                for mi in motsInterdits :
                    if(m == mi) :
                        isInterdit = True
                        break
                if(not isInterdit) : mots.append(m)
        counts = Counter(mots)
        self.mot1 = max(counts, key=counts.get)

if __name__ == '__main__':
    rss = FluxRss()
    t0 = 0
    t1 = 0
    while True:
        maintenant = time.time()
        if(maintenant-t1>3600): # toutes les heures
            rss.maj()
            t1 = maintenant
        if(maintenant-t0>1): # toutes les 1 secondes
            print()
            print(rss.getTitreRandom())
            print("Mot1 = " + rss.mot1)
            print("---------------------------------------")
            t0 = maintenant
