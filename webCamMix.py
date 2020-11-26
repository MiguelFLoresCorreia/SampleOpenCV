# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 09:01:03 2020

@author: robin
"""

import numpy as np
import cv2
import time
import pygame.mixer
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

Tk().withdraw() 
dirname = askdirectory()
tabMusiques = os.listdir(dirname)

piano = False

cap=cv2.VideoCapture(0)

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w, h)

ymin=0
ymax=int(h/4)

nbMusiques = len(tabMusiques)

if(nbMusiques>10):
    nbMusiques=10
print(nbMusiques)
w=int(w/len(tabMusiques))

old=[]
timeS=[]
xmin=[]
xmax=[]
for i in range(nbMusiques):
    old.append(0)
    timeS.append(time.time()+3)
    if len(xmin)==0:
        xmin.append(0)
    else:    
        xmin.append(xmax[i-1])
    if len(xmax)==0:
        xmax.append(w)
    else:    
        xmax.append(xmin[i]+w)

kernel_blur=5
seuil=20
surface=1000
ret, originale=cap.read()
originale=cv2.cvtColor(originale, cv2.COLOR_BGR2GRAY)
originale=cv2.GaussianBlur(originale, (kernel_blur, kernel_blur), 0)
kernel_dilate=np.ones((5, 5), np.uint8)

def calcul_mean(image):
    height, width=image.shape
    s=0
    for y in range(height):
        for x in range(width):
            s+=image[y][x]
    return s/(height*width)

def imshow_fullscreen (winname, img):
    cv2.namedWindow (winname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty (winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow (winname, img)

dj=[]
pygame.mixer.init()
# chargement de la musique
for i in range(nbMusiques):
    print(tabMusiques[i])
    musiqueAAjouter=pygame.mixer.Sound(dirname+"/"+tabMusiques[i])
    pygame.mixer.Channel(i).play(musiqueAAjouter, loops=-1)
    musiqueAAjouter.set_volume(0)
    dj.append(musiqueAAjouter)

while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    
    if(piano):
        print("piano")
        for i in range(len(old)):
            if calcul_mean(mask[0:ymax-ymin, xmin[i]-xmin[0]:xmax[i]-xmin[0]])> seuil:
                if old[i]==0:
                    old[i]=1
                    timeS[i] = time.time()
                    dj[i].stop()
                    dj[i].play()
                    dj[i].set_volume(1)
            if(time.time() - timeS[i]) >= 0.5:
                old[i]=0
                dj[i].set_volume(0)
            cv2.rectangle(frame, (xmin[i], ymin), (xmax[i], ymax), (0, 0, 255) if old[i] else (255, 0, 0), 3)
    else:
        for i in range(len(old)):
            if(time.time() - timeS[0]) >= 1:
                if calcul_mean(mask[0:ymax-ymin, xmin[i]-xmin[0]:xmax[i]-xmin[0]])> seuil:
                    if old[i]==0:
                        old[i]=1
                        timeS[0] = time.time()
                        dj[i].set_volume(1)
                    elif old[i]==1:
                        old[i]=0
                        timeS[0] = time.time()
                        dj[i].set_volume(0)
            cv2.rectangle(frame, (xmin[i], ymin), (xmax[i], ymax), (0, 0, 255) if old[i] else (255, 0, 0), 3)
    
    originale=gray
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "PIANO: {:d}".format(piano), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    imshow_fullscreen ('frame', frame)
    
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        pygame.mixer.quit()
        break
    if key==ord('p'):
        piano=not piano
        

cap.release()
cv2.destroyAllWindows()