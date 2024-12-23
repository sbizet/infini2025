#Classe regroupant les spécificités de la structure sur laquelle les chariots circulent.
from math import atan, sqrt,sin,cos,pi
class Structure :
    def __init__(self):
        self.l = 1.5 # la longueur des parties linéaires du rail en m
        self.R = 0.61 #le rayon des cercles en m
        self.echelle = 100 # en pixel par m

        self.alpha = atan(2*self.R/self.l) # pente en rad de la partie linéaire
        self.xc = sqrt(self.R*self.R+(self.l/2)*(self.l/2)) # abscisse du centre des arcs cercle

    def affiche(self,c,echelle):
        self.echelle = echelle
        alpha = self.alpha
        l=self.l
        xc = self.xc
        R = self.R
        #on se place au centre du canvas
        x=int(c['width'])/2 
        y=int(c['height'])/2
        # On dessine la structure
        c.create_line(x-l*echelle*cos(alpha)/2,y-l*echelle*sin(alpha)/2,x+l*echelle*cos(alpha)/2,y+l*echelle*sin(alpha)/2, fill="red", width=2)
        c.create_line(x-l*echelle*cos(alpha)/2,y+l*echelle*sin(alpha)/2,x+l*echelle*cos(alpha)/2,y-l*echelle*sin(alpha)/2, fill="red", width=2)
        c.create_arc(x+(xc-R)*echelle,y-R*echelle,x+(xc+R)*echelle,y+R*echelle,style='arc',start=90+alpha*180/pi,extent=-180-2*alpha*180/pi, outline="red", width=2)
        c.create_arc(x+(-xc-R)*echelle,y-R*echelle,x+(-xc+R)*echelle,y+R*echelle,style='arc',start=90-alpha*180/pi,extent=180+2*alpha*180/pi, outline="red", width=2)

if __name__ == '__main__':
    from tkinter import Tk,Canvas
    root = Tk()
    root.geometry("400x400")
    structure = Structure()
    visu = Canvas(root, bg="lightgray", height=200, width=400)
    visu.pack()
    structure.affiche(visu,100)
    root.mainloop()
