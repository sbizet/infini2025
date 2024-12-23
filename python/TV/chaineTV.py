import tkinter as tk
import tkinter.font as tkFont
from PIL import Image,ImageTk
from Camera import Video
from scrapX import FuckX
from FluxRss import FluxRss
import time
import random
import math
import threading

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) # permet d'ignorer scaling 150% par Windows

root = tk.Tk()

root.geometry("1366x768+0+0")

class TvChannel :
    def __init__(self, master,id):
        if(id == "uLive") : self.colors = ['#00186A','#156CFF','#FFF300','#FFFFFF']
        if(id == "fourstream") : self.colors = ['#D42300', '#FF8571', '#00186A', '#FFFFFF']
        self.id = id
        self.master = master
        self.canvas = tk.Canvas(master, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.text1 = "HELLO WORLD"
        self.text2 = "HELLO WORLD"
        self.text3 = "HELLO WORLD"
        self.text4 = "HELLO WORLD"
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0
        self.bandeauxAff()
        self.rss = FluxRss()
        self.twitter = FuckX()
        threading.Thread(target=self.initVideo).start()
        self.video = None
        self.majVideo()

    def initVideo(self):
        self.video = Video(self.canvas) # long et bloquant

    def bandeauxAff(self):
        self.rectangleZ1 = self.canvas.create_rectangle(244, 548, 244+285, 548+51, fill=self.colors[2])
        self.textZ1 = self.canvas.create_text(244+15, 548+50/2, text=self.text1, fill=self.colors[0], font=tkFont.Font(family="Helvetica",size=14,weight="bold"), anchor=tk.W)
        self.rectangleZ2 = self.canvas.create_rectangle(244, 590, 244+1122, 590+78, fill=self.colors[0])
        self.textZ2 = self.canvas.create_text(244+15, 590+78/2, text=self.text2, fill=self.colors[3], font=tkFont.Font(family="Helvetica",size=18,weight="bold"), anchor=tk.W)
        self.rectangleZ3 = self.canvas.create_rectangle(0, 667, 0+1366, 667+50, fill=self.colors[1])
        self.textZ3 = self.canvas.create_text(0+15, 667+50/2, text=self.text3, fill=self.colors[0], font=tkFont.Font(family="Helvetica",size=14,weight="bold"), anchor=tk.W)
        self.rectangleZ4 = self.canvas.create_rectangle(0, 718, 0+1366, 718+50, fill=self.colors[2])
        self.textZ4 = self.canvas.create_text(0+15, 718+50/2, text=self.text4, fill=self.colors[0], font=tkFont.Font(family="Helvetica",size=14,weight="bold"), anchor=tk.W)
        self.imgLogo= ImageTk.PhotoImage(Image.open("./"+self.id+"/logo.png"))
        self.canvas.create_image(70,54,anchor=tk.NW,image=self.imgLogo)
        self.img24h= ImageTk.PhotoImage(Image.open("./"+self.id+"/24h.png"))
        self.canvas.create_image(58,560,anchor=tk.NW,image=self.img24h)

    def majVideo(self):
        self.canvas.delete('all') # peut être inutile ...
        if(self.video != None) : self.video.update()
        self.bandeauxAff()
        self.setText()
        self.master.after(15,self.majVideo)

    def setText(self):
        maintenant = time.time()
        if (maintenant - self.t1 > 5) :
            self.t1 = maintenant
            self.text1 = self.rss.mot1
            self.text2 = self.rss.getTitreRandom()
            self.text3 = self.twitter.getDernierTweet()
        if(maintenant - self.t2 > 3600) :
            self.t2 = maintenant
            self.rss.maj()
        if (maintenant - self.t3 > 1000) :
            self.t3 = maintenant
            self.twitter.majThread()
        if(maintenant - self.t4 > 0.3) :
            self.text4 = "info : "+ "%.3f" % (6*random.random() -3) + " \t\t| "
            self.text4 +="tendance : "+ "%.3f" % (888*math.sin(1E-2*(maintenant-self.t2))) + " \t\t| "
            self.text4 += "cours : " + "%.2f" % ((maintenant - self.t4)*100) + " %"
            self.t4 = maintenant

fourstream = TvChannel(root,"fourstream")

root.mainloop()
