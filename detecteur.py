# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 09:01:03 2020

@author: robin
"""

import numpy as np
import cv2
import time
import pygame.mixer

cap=cv2.VideoCapture(0)

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w, h)

ymin=0
ymax=int(h/4)

w=int(w/5)

xmin1=0
xmax1=w

xmin2=w
xmax2=xmin2+w

xmin3=xmax2
xmax3=xmin3+w

xmin4=xmax3
xmax4=xmin4+w

xmin5=xmax4
xmax5=xmin5+w

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

old_1=0
old_2=0
old_3=0
old_4=0
old_5=0

timeS = time.time()+5

pygame.mixer.init()
# chargement de la musique
musique1=pygame.mixer.Sound("musiques/bass90.wav")
musique2=pygame.mixer.Sound("musiques/batterie90.wav")
musique3=pygame.mixer.Sound("musiques/gated90.wav")
musique4=pygame.mixer.Sound("musiques/percutguitare90.wav")
musique5=pygame.mixer.Sound("musiques/beat90.wav")
pygame.mixer.Channel(1).play(musique1, loops=-1)
pygame.mixer.Channel(2).play(musique2, loops=-1)
pygame.mixer.Channel(3).play(musique3, loops=-1)
pygame.mixer.Channel(4).play(musique4, loops=-1)
pygame.mixer.Channel(5).play(musique5, loops=-1)
musique1.set_volume(0)
musique2.set_volume(0)
musique3.set_volume(0)
musique4.set_volume(0)
musique5.set_volume(0)

while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    
    if(time.time() - timeS) >= 1:
        if calcul_mean(mask[0:ymax-ymin, 0:xmax1-xmin1])> seuil:
            if old_1==0:
                old_1=1
                timeS = time.time()
                print("play 1")
                musique1.set_volume(1)
            elif old_1==1:
                old_1=0
                timeS = time.time()
                print("stop 1")
                musique1.set_volume(0)
            
        if calcul_mean(mask[0:ymax-ymin, xmin2-xmin1:xmax2-xmin1])> seuil:
            if old_2==0:
                old_2=1
                timeS = time.time()
                print("play 2")
                musique2.set_volume(1)
            elif old_2==1:
                old_2=0
                timeS = time.time()
                print("stop 2")
                musique2.set_volume(0)
                
        if calcul_mean(mask[0:ymax-ymin, xmin3-xmin1:xmax3-xmin1])> seuil:
            if old_3==0:
                old_3=1
                timeS = time.time()
                print("play 3")
                musique3.set_volume(1)
            elif old_3==1:
                old_3=0
                timeS = time.time()
                print("stop 3")
                musique3.set_volume(0)
                
        if calcul_mean(mask[0:ymax-ymin, xmin4-xmin1:xmax4-xmin1])> seuil:
            if old_4==0:
                old_4=1
                timeS = time.time()
                print("play 4")
                musique4.set_volume(1)
            elif old_4==1:
                old_4=0
                timeS = time.time()
                print("stop 4")
                musique4.set_volume(0)
                
        if calcul_mean(mask[0:ymax-ymin, xmin5-xmin1:xmax5-xmin1])> seuil:
            if old_5==0:
                old_5=1
                timeS = time.time()
                print("play 5")
                musique5.set_volume(1)
            elif old_5==1:
                old_5=0
                timeS = time.time()
                print("stop 5")
                musique5.set_volume(0)

    originale=gray
    
    cv2.rectangle(frame, (xmin1, ymin), (xmax1, ymax), (0, 0, 255) if old_1 else (255, 0, 0), 3)
    cv2.rectangle(frame, (xmin2, ymin), (xmax2, ymax), (0, 0, 255) if old_2 else (255, 0, 0), 3)
    cv2.rectangle(frame, (xmin3, ymin), (xmax3, ymax), (0, 0, 255) if old_3 else (255, 0, 0), 3)
    cv2.rectangle(frame, (xmin4, ymin), (xmax4, ymax), (0, 0, 255) if old_4 else (255, 0, 0), 3)
    cv2.rectangle(frame, (xmin5, ymin), (xmax5, ymax), (0, 0, 255) if old_5 else (255, 0, 0), 3)
    
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