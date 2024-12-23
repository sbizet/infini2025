from websockets.sync.server import serve
import threading


class InterfaceWs :
    def __init__(self):
        t1 = threading.Thread(target=self.startServeur)
        t1.start()
        self.websocket = None
        self.maj = False
        self.trameEnvoi = [65,1,100,0,255,0,0,0]
        self.trameRecue = [65,200,150,100,101,0,0,0]

    def decodeTrame(self,s):
        tabHex = [s[i:i+2] for i in range(0, len(s), 2)]
        tabRetour = []
        for valHex in tabHex :
            tabRetour.append(int(valHex, 16))
        return tabRetour

    def encodeTrame(self,tab):
        retour = ""
        for val in tab :
            retour += "{:02x}".format(val)
        return retour

    def handler(self,websocket):
        self.websocket = websocket
        while True:
            if(self.maj) :
                self.maj = False
                websocket.send(self.encodeTrame(self.trameEnvoi))
                messageBrut = websocket.recv()
                self.trameRecue=self.decodeTrame(messageBrut)

    def startServeur(self):
        with serve(self.handler, "", 8484) as server:
            server.serve_forever()

# Test unitaire
if __name__ == '__main__':
    import time
    t0 = time.time()
    ws = InterfaceWs()
    while True:
        maintenant = time.time()
        if(maintenant-t0>0.1):
            t0 = maintenant
            ws.maj=True

"""
Trame envoyée
Octet n° 0 : 65 ou 66 ('A' ou 'B' en ASCII) : information sur le chariot concerné A ou B
Octet n°1 : 0 ou 1 : le chariot est mis en marche ou arrêté.
Octet n°2 : 0 à 255 : Vmot = information pour le réglage de la vitesse du moteur
Octet n°3 : 0 à 180 : Pan
Octet n°4 : 0 à 180 : Tilt
Octet n°5 : 0 octet bidon
Octet n°6 : 0 octet bidon
Octet n°7 : 0 octet bidon

Trame reçue :
Octet n°0 : 65 ou 66 ('A' ou 'B' en ASCII) : information sur le chariot A ou B envoyant l'information
Octet n°1 : Vbat (0 à 255) : Une information sur la tension au niveau de la batterie (255 correspondant à 15V par exemple)
Octet n°2 : inclinaison  (0 à 255) information issue de l'accélérometre + gyroscope
Octet n°3 : wr (0 à 255) information issue de l'accélérometre + gyroscope
Octet n°4 : vR (0 à 255) : vitesse réelle
Octet n°5 : 0 octet bidon
Octet n°6 : 0 octet bidon
Octet n°7 : 0 octet bidon
"""
