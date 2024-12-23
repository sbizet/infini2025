from tkinter import Tk,Canvas,Button,CENTER,NW
import cv2
import PIL.Image, PIL.ImageTk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) # permet d'ignorer scaling 150% par Windows

class Video:
    def __init__(self, canvas, video_source=0):
        self.canvas = canvas
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.image = None

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            if(self.image != None) : self.canvas.delete(self.image)
            PILImage = PIL.Image.fromarray(frame)
            #PILImage = PILImage.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
            PILImage = self.redimCrop(PILImage,self.canvas.winfo_width(), self.canvas.winfo_height())
            self.photo = PIL.ImageTk.PhotoImage(image = PILImage)
            self.image = self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

    def redimCrop(self,im,wCible,hCible):
        w, h = im.size
        ratio = w / h
        ratioCible = wCible/hCible
        if(ratioCible<ratio):
            imR = im.resize((int(w*hCible/h),hCible))
            # ligne suivante = à vérifier ...
            retour = imR.crop((int((-wCible+w*hCible/h)/2),0, wCible+int((-wCible+w*hCible/h)/2),hCible))
        else:
            imR = im.resize((wCible,int(h*wCible/w)))
            retour = imR.crop((0, int((-hCible+h*wCible/w)/2),wCible,hCible+int((-hCible+h*wCible/w)/2)))
        return retour

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == '__main__':
    fenetreTV = Tk()
    #app = App(fenetreTV, "http://192.168.1.197:81/stream")

    canvas = Canvas(fenetreTV, width = 1366, height = 768)
    canvas.pack()
    video = Video(canvas)
    def maj():
        video.update()
        fenetreTV.after(15,maj)
    maj()
    fenetreTV.mainloop()
