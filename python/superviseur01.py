from InterfaceWs import InterfaceWs
from Chariot import Chariot
from Gui import Gui
from tkinter import Tk,Toplevel


chariotA = Chariot(65)
chariotB = Chariot(66)

ws = InterfaceWs()

fenetreSuperviseur = Tk()
fenetreSuperviseur.geometry("800x600")
gui = Gui(fenetreSuperviseur,chariotA,chariotB)

def maj():
    ws.trameEnvoi = chariotA.getTrameEnvoi()
    ws.maj = True
    chariotA.maj(ws.trameRecue)
    gui.maj()
    fenetreSuperviseur.after(15,maj)
fenetreSuperviseur.after(15,maj)

fenetreSuperviseur.mainloop()
