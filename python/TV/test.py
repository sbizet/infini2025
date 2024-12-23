import PIL.Image, PIL.ImageTk


def redimMarge(im,wCible,hCible):
    w, h = im.size
    ratio = w / h
    ratioCible = wCible/hCible
    if(ratioCible>ratio):
        imR = im.resize((int(w*hCible/h),hCible))
        retour = PIL.Image.new(mode = "RGB", size = (wCible, hCible), color = (128, 128, 128))
        retour.paste(imR, (int((wCible-w*hCible/h)/2), 0))
    else:
        imR = im.resize((wCible,int(h*wCible/w)))
        retour = PIL.Image.new(imR.mode, (wCible, hCible), (128, 128, 128))
        retour.paste(imR, (0, int((hCible-h*wCible/w)/2)))
    return retour

def redimCrop(im,wCible,hCible):
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

im = PIL.Image.open('lena.gif')
#im = redimMarge(im,1366,768)
im = redimCrop(im,1366,768)
im.show()
