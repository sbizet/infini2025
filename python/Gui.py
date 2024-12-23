from tkinter import Tk, Label, Button, Canvas, Scale, HORIZONTAL,Toplevel
from Structure import Structure
import math


class Gui:
    def __init__(self, master,chariotA,chariotB):
        self.master = master

        master.title("Superviseur")

        self.chariotA = chariotA
        self.chariotB = chariotB
        self.boutonMarche = Button(master, text="Marche", command=self.marche, height=1, width=20)
        self.boutonMarche.pack()

        self.boutonArret = Button(master, text="Arret", command=self.arret, height=1, width=20)
        self.boutonArret.pack()

        self.structure = Structure()
        self.chariotA.structure = self.structure
        self.chariotB.structure = self.structure
        self.visu = Canvas(master, bg="lightgray", height=300, width=600)
        self.structure.affiche(self.visu,150)
        self.visu.pack()

        Button(master, text="Quit", command=master.destroy).pack()

        self.boiteA = self.visu.create_polygon([(0, 0), (10, 0), (10, 10), (0, 10)], fill="green")
        self.labelInfo = Label(master , text = "...",justify = "left")
        self.labelInfo.pack()

        self.sliderVMotA = Scale(master, from_=0, to=255, orient=HORIZONTAL,length=600,command=self.majVMotA)
        self.sliderVMotA.pack()

        self.sliderPanA = Scale(master, from_=0, to=255, orient=HORIZONTAL,length=600,command=self.majPanA)
        self.sliderPanA.pack()

        self.sliderTiltA = Scale(master, from_=0, to=255, orient=HORIZONTAL,length=600,command=self.majTiltA)
        self.sliderTiltA.pack()

    def majVMotA(self,event):
        self.chariotA.setVMot(self.sliderVMotA.get())
    def majPanA(self,event):
        self.chariotA.setPan(self.sliderPanA.get())
    def majTiltA(self,event):
        self.chariotA.setTilt(self.sliderTiltA.get())

    def translationRotation(self,boite,x,y,angle):
        points = [(-5, -5), (5, -5), (5, 5), (-5, 5)]
        nouveauxPoints = []
        ei = complex(math.cos(angle),math.sin(angle))
        for (xx,yy) in points:
            v = ei * complex(xx, yy)
            nouveauxPoints.append(v.real+x)
            nouveauxPoints.append(v.imag+y)
            self.visu.coords(boite, *nouveauxPoints)

    def maj(self):
        info = self.chariotA.getInfo()
        self.labelInfo.config(text=info)
        x=int(self.visu['width'])/2 + self.structure.echelle*self.chariotA.x
        y=int(self.visu['height'])/2 + self.structure.echelle*self.chariotA.y

        if(self.chariotA.posDetecte):
            self.translationRotation(self.boiteA,x,y,math.pi/2-self.chariotA.inclinaisonCalculee)

    def marche(self):
        self.chariotA.setOn(1)

    def arret(self):
        self.chariotA.setOn(0)

if __name__ == '__main__':
    fenetreSuperviseur = Tk()
    fenetreSuperviseur.geometry("800x600")
    from Chariot import Chariot
    chariotA = Chariot(65)
    chariotB = Chariot(66)
    chariotA.posDetecte = True
    gui = Gui(fenetreSuperviseur,chariotA,chariotB)
    gui.maj()
    fenetreSuperviseur.mainloop()
