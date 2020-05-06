import cv2
import math
import numpy as np

def PROCESSING(path):
    img=cv2.imread(path)
    cv2.imshow("Original",img)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hue,saturation,value=cv2.split(hsv)
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    topHat=cv2.morphologyEx(value,cv2.MORPH_TOPHAT,kernel)
    blackHat=cv2.morphologyEx(value,cv2.MORPH_BLACKHAT,kernel)
    addimg=cv2.add(value,topHat)
    subtractimg=cv2.subtract(addimg,blackHat)
    blur=cv2.GaussianBlur(subtractimg,(5,5),0)
    thresholdimage=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,19,9)
    if int(cv2.__version__.split(".")[0])>=4:
        contours,hierarchy=cv2.findContours(thresholdimage,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    else:
        imageContours, contours, hierarchy = cv2.findContours(thresholdimage,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    height,width=thresholdimage.shape
    return (height,width,contours)
