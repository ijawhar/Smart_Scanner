from tkinter import *
import urllib
import cv2
import numpy as np
import requests as r
from PIL import Image, ImageTk
import pytesseract
import time
from matplotlib import pyplot as plt

class MyWindow(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        zone1 = Frame(self)
        self.urlStr = StringVar()
        self.urlStr.set('adresse IP:Port')
        labelUrl = Label( zone1, text="Url de connexion:")
        labelUrl.pack(side=LEFT)
        url = Entry(zone1, textvariable=self.urlStr )
        url.focus_set()
        url.pack(side=LEFT)
        button = Button(zone1, text="Connexion", command=self.doConnexion)
        button.pack()
        zone1.pack()

      
    def doConnexion(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        server_url = self.urlStr.get()
        url = 'http://'+ server_url +'/shot.jpg'
        print(url)
        while True:
            img = urllib.request.urlopen(url)
            img_bytes = bytearray(img.read())   
            img_np = np.array(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_np,1)
            cv2.imshow('My Smart Scanner', frame )
            ch = cv2.waitKey(1)
            if ch == ord('s'):
                img_pil = Image.fromarray(frame)
                img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                img_tr = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                img_blur = cv2.medianBlur(img_tr,1)
                texteCI = pytesseract.image_to_string(img_blur)
                test = str(texteCI)
                testLower = str(test.lower())
                print(testLower)
                ss = testLower.split()
                print(ss)

                time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S')
                dirCascadeFiles = r'../opencv/'
                cascadefile = dirCascadeFiles + "haarcascade_frontalface_alt.xml" 
                #classCascade = cv2.CascadeClassifier("D:/Master2_Info/projets/iot/SmartScanner/opencv/haarcascade_frontalface_alt.xml")
                classCascade = cv2.CascadeClassifier("opencv\haarcascade_frontalface_alt.xml")
                faces = classCascade.detectMultiScale(img_gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)
                print("Il y a {0} visage(s).".format(len(faces)))
                list1 = ['permis', 'conduire', 'carte', 'nationale', 'republique', 'francaise','titre', 'séjour','PASSEPORT', 'PASSPORT','passport', 'passeport']
                list2= ['facture', 'FACTURE','Avis', 'échéance','client','détail échéance','référence']
                trouver = False
                chercher = False
                for i in range(len(list1)):
                    if(testLower.find(list1[i]) !=-1):
                        trouver = True    
                        break
                for i in range(len(list2)):
                    if(testLower.find(list2[i]) !=-1):
                        chercher = True    
                        break

                if(trouver and len(faces) !=0):
                    img_pil.save(f'Pieces_Identite/scan-doc-{time_stamp}.pdf')
                    print('save1')
                elif(chercher !=0):
                    img_pil.save(f'Facture/scan-doc-{time_stamp}.pdf')
                    print('save3')
                else:
                    img_pil.save(f'Divers/scan-doc-{time_stamp}.pdf')
                    print('save2')
                    
            if ch == 27 or ch == ord('q') or ch == ord('Q'):
                cv2.destroyAllWindows()
                break
     
  
window = MyWindow()
photo = PhotoImage(file="scan2.png")
canvas = Canvas(window,width=500, height=500)
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()
window.mainloop()