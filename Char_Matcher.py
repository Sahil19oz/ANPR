import cv2
import numpy as np
from Auxillary import Functions

def matchingChars(char,listofchar):
    all_chars=[]
    for i in listofchar:
        if i==listofchar:
            continue
    #compute parameters to see if chars are matching
        Distance=Functions.distanceBetweenChars(char,i)
        angle=Functions.angleBetweenChars(char,i)
        dArea=abs(i.boundingRectArea-char.boundingRectArea)/char.boundingRectArea
        dWidth=abs(i.boundingRectWidth-char.boundingRectWidth)/char.boundingRectWidth
        dHeight=abs(i.boundingRectHeight-char.boundingRectHeight)/char.boundingRectHeight

        # check if chars match
        if Distance<(char.diagonalSize*5) and angle<12.0 and dArea<0.5 and dWidth<0.8 and dHeight<0.2:
                all_chars.append(i)
                
        return all_chars
