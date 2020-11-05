# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 09:01:03 2020

@author: robin
"""

import numpy as np
import cv2
import pygame.mixer

cap=cv2.VideoCapture(0)

ymin=0
ymax=100

xmin1=0
xmax1=100

xmin2=300
xmax2=400

xmin3=550
xmax3=638

kernel_blur=5
seuil=50
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

old_1=0
old_2=0
old_3=0

test=0

pygame.mixer.init()
pygame.mixer.music.load("musique.mp3")   # chargement de la musique
pygame.mixer.music.play()
pygame.mixer.music.pause()

while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    contours, nada=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_contour=frame.copy()
    
    if calcul_mean(mask[0:ymax-ymin, 0:xmax1-xmin1])> seuil:
        if old_1==0:
            old_1=1
            print("play")
            pygame.mixer.music.unpause()
        elif old_1==1:
            old_1=0
            print("stop")
            pygame.mixer.music.pause()
        

        
        
    for c in contours:
        cv2.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv2.contourArea(c)<surface:
            continue
        x, y, w, h=cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    originale=gray
    frame = cv2.flip(frame, 1)
    frame_contour = cv2.flip(frame_contour, 1)
    cv2.putText(frame_contour, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    
    mask = cv2.flip(mask, 1)
    
    cv2.rectangle(frame_contour, (xmin1, ymin), (xmax1, ymax), (0, 0, 255) if old_1 else (255, 0, 0), 3)
    cv2.rectangle(frame_contour, (xmin2, ymin), (xmax2, ymax), (0, 0, 255) if old_2 else (255, 0, 0), 3)
    cv2.rectangle(frame_contour, (xmin3, ymin), (xmax3, ymax), (0, 0, 255) if old_3 else (255, 0, 0), 3)
    
  #  cv2.imshow("frame", frame)
    cv2.imshow("contour", frame_contour)
#    cv2.imshow("mask", mask)
    intrus=0
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        pygame.mixer.music.stop()
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