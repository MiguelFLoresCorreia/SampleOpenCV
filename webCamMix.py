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
xmin=[]
xmax=[]
for i in range(nbMusiques):
    old.append(0)
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

timeS = time.time()+5

dj=[]
pygame.mixer.init()
# chargement de la musique
i=0 
for musique in range(nbMusiques):
    print(tabMusiques[musique])
    musiqueAAjouter=pygame.mixer.Sound(dirname+"/"+tabMusiques[musique])
    pygame.mixer.Channel(i).play(musiqueAAjouter, loops=-1)
    musiqueAAjouter.set_volume(0)
    dj.append(musiqueAAjouter)
    i=i+1

while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    
    for i in range(len(old)):
        if(time.time() - timeS) >= 1:
            if calcul_mean(mask[0:ymax-ymin, xmin[i]-xmin[0]:xmax[i]-xmin[0]])> seuil:
                if old[i]==0:
                    old[i]=1
                    timeS = time.time()
                    dj[i].set_volume(1)
                    print(old[i])
                elif old[i]==1:
                    old[i]=0
                    timeS = time.time()
                    dj[i].set_volume(0)
        cv2.rectangle(frame, (xmin[i], ymin), (xmax[i], ymax), (0, 0, 255) if old[i] else (255, 0, 0), 3)
    
    originale=gray
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    imshow_fullscreen ('frame', frame)
    
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        pygame.mixer.quit()
        break
    if key==ord('p'):
        kernel_blur=min(43, kernel_blur+2)
    if key==ord('m'):
        kernel_blur=max(1, kernel_blur-2)
    if key==ord('i'):
        surface+=1000
    if key==ord('k'):
        surface=max(1000, surface-1000)
    if key==ord('o'):
        seuil=min(255, seuil+1)
    if key==ord('l'):
        seuil=max(1, seuil-1)

cap.release()
cv2.destroyAllWindows()