from math import pi,cos,sin
import time

class Chariot :
    def __init__(self,id):
        self.id = id # 'A' ou 'B'
        self.trameEnvoi = [id,0,0,0,0,0,0,0] # valeur par défaut
        self.trameRecue = [id,0,0,0,0,0,0,0] # valeur par défaut
        self.vRotMax = 120
        self.perimetreRoue = pi*0.1
        self.vMax = (self.perimetreRoue*self.vRotMax)/60
        self.structure = None
        self.x = 0
        self.y = 0
        self.phase = -1
        self.dPhase = -1
        self.inclinaisonMesuree = 0
        self.wr = 0
        self.v = 0
        self.inclinaisonCalculee = 0
        self.posDetecte = False
        self.to = time.time()

    def maj(self,trameRecue):
        self.trameRecue = trameRecue
        self.inclinaisonMesuree = 2*pi*self.getInclinaisonRecu()/255.0-pi
        self.wr = 1.5*(2*2.5*self.getWrRecu()/255.0 - 2.5);
        self.v = (self.getVRRecu()*self.vMax)/255;
        self.calcCoord()

    def calcCoord(self):
        oldPhase = self.phase
        self.phase = self.detectPhase()
        maintenant = time.time()
        if(self.phase != oldPhase and oldPhase != -1 ) :
            self.dPhase = 0
            self.posDetecte = True
        else :
            self.dPhase += self.v*(maintenant-self.to)
        self.to = maintenant
        st = self.structure
        if (self.phase == 1) :
            self.inclinaisonCalculee = pi/2 + st.alpha
            x0 = -st.xc-st.R*cos(pi/2 + st.alpha)
            y0 = st.R*sin(pi/2 + st.alpha)
            self.x = x0 + self.dPhase*cos(st.alpha)
            self.y = y0 - self.dPhase*sin(st.alpha)

        if (self.phase == 2) :
            inclinaisonInitiale = pi/2 + st.alpha
            self.inclinaisonCalculee=-self.dPhase/st.R+inclinaisonInitiale
            self.x = st.xc + st.R*cos(self.inclinaisonCalculee)
            self.y = -st.R*sin(self.inclinaisonCalculee)

        if (self.phase == 3) :
            self.inclinaisonCalculee = -pi/2 - st.alpha
            x0 = st.xc+st.R*cos(-pi/2 - st.alpha)
            y0 = -st.R*sin(-pi/2 - st.alpha)
            self.x = x0 - self.dPhase*cos(st.alpha)
            self.y = y0 - self.dPhase*sin(st.alpha)

        if (self.phase == 4) :
            inclinaisonInitiale = - pi/2 - st.alpha
            self.inclinaisonCalculee= +self.dPhase/st.R+inclinaisonInitiale
            self.x = -st.xc - st.R*cos(self.inclinaisonCalculee)
            self.y = st.R*sin(self.inclinaisonCalculee)



    def detectPhase(self):
        if (self.v<0.05) :
            #TO DO
            #il faut trouver une stratégie pour détecter les changement de phase à faible vitesse. Peut être l'inclinaison ... qui est peu bruitée.
            #print("vitesse trop faible pour détecter changement de phase")
            return self.phase

        seuilBasWr = 0.4*self.v
        seuilHautWr = 0.8*self.v
        seuilInclinaison = 0.3
        if (self.inclinaisonMesuree>seuilInclinaison and abs(self.wr)<seuilBasWr) : return 1
        if (self.wr<(-seuilHautWr))  : return 2
        if (self.inclinaisonMesuree<(-seuilInclinaison) and abs(self.wr)<seuilBasWr) : return 3
        if (self.wr>seuilHautWr) : return 4
        self.posDetecte = False
        return self.phase

    def getTrameEnvoi(self):
        return self.trameEnvoi

    def getOn(self):
        return self.trameEnvoi[1]

    def setOn(self,on):
        self.trameEnvoi[1] = on

    def setVMot(self,vMot):
        self.trameEnvoi[2] = vMot

    def setPan(self,pan):
        self.trameEnvoi[3] = pan

    def setTilt(self,tilt):
        self.trameEnvoi[4] = tilt

    def getVBatRecu(self):
        return self.trameRecue[1]

    def getInclinaisonRecu(self):
        return self.trameRecue[2]

    def getWrRecu(self):
        return self.trameRecue[3]

    def getVRRecu(self):
        return self.trameRecue[4] # vitesse réelle mesurée

    def getInfo(self):
        s = self.trameRecue
        info = "Chariot = " + chr(s[0]) + "\n"
        info += "vBat = " + str(s[1]) + "\n"
        info += "inclinaison = " + str(s[2]) + "\n"
        info += "wr = " + str(s[3]) + "\n"
        info += "vR = " + str(s[4]) + "\n"
        return info
