from cv2 import *
import math
import os
import numpy as np
from Char_Recognition import OCR
from Auxillary import Functions

def POSSIBLEPLATES(path,height,width,contours):
    #create a numpy array with shape of given dimensions
    img=imread("C:\\Users\\home\\Desktop\\project\\test_data\\"+str(path))
    imageC=np.zeros((height,width,3),dtype=np.uint8)
    #Possible chars
    chars=[]
    count=0
    #We need to check the possility of encoumtering possible plates with char count>7
    for i in range(len(contours)):
          drawContours(imageC,contours,i,(255,255,255))
          #retrieve possible chars from this contours
          c=Functions.ifChar(contours[i])
          if Functions.checkIfChar(c):
              count+=1
              chars.append(c)
    imageC=np.zeros((height,width,3),np.uint8)
    Possiblechar=[]
    for i in chars:
        Possiblechar.append(i.contour)
    drawContours(imageC,Possiblechar,-1,(255,255,255))

    #Now we will find the most appropriate plate in all the contours that we have encountered
    plates=[]
    matchingchars=[]
    for c in chars:
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

        #here we are reaaranging all the possible plate characterization
        charsfound=matchingChars(c,chars)
        charsfound.append(c)

        #check if current matching char satifies the len of possible plates
        if len(charsfound)<3:
            continue
        matchingchars.append(charsfound)
        newlist=list(set(chars)-set(charsfound))
        recursivelist=[]
        for charlist in recursivelist:
            matchingchars.append(charlist)
        break

    imageC=np.zeros((height,width,3),np.uint8)
    for chars in matchingchars:
        color=(255,0,255)
        contours=[]
        for matchingchar in chars:
            contours.append(matchingchar.contour)
        drawContours(imageC,contours,-1,color)
    for chars in matchingchars:
        possibleplate=Functions.PossiblePlate()
        chars.sort(key=lambda matchingchar:matchingchar.centerX)
        #calculate the center point of plate
        XC=(chars[0].centerX+chars[len(chars)-1].centerX)/2
        YC=(chars[0].centerY+chars[len(chars)-1].centerY)/2
        center=XC,YC
        platewidth=int((chars[len(chars)-1].boundingRectX+chars[len(chars)-1].boundingRectWidth-chars[0].boundingRectX)*1.3)
        totalheight=0
        for char in chars:
            totalheight+=char.boundingRectHeight
        averageheight=totalheight/len(chars)
        plateheight=int(averageheight*1.5)
        #calculate corretion angle of plate region
        opposite=chars[len(chars)-1].centerY-chars[0].centerY
        hypotenuse=Functions.distanceBetweenChars(chars[0],chars[len(chars)-1])
        AngleRAD=math.asin(opposite/hypotenuse)
        AngleDEG=AngleRAD*(180.0/math.pi)
        possibleplate.rrLocationOfPlateInScene=(tuple(center),(platewidth,plateheight),AngleDEG)
        #Get  the rotation matric
        rmatrix=getRotationMatrix2D(tuple(center),AngleDEG,1.0)
        height,width,channel=img.shape

        #rotate the enire image
        imgrotated=warpAffine(img,rmatrix,(width,height))
        #crop the detected plate
        imgcropped=getRectSubPix(imgrotated,(platewidth,plateheight),tuple(center))
        possibleplate.Plate=imgcropped
        if possibleplate.Plate is not None:
            plates.append(possibleplate)

        #draw the region of interest on original image
        for i in range(len(plates)):
            rectpoints=boxPoints(plates[i].rrLocationOfPlateInScene)
            rectcolor=(0,255,0)
            line(img,tuple(rectpoints[0]),tuple(rectpoints[1]),rectcolor,2)
            line(img,tuple(rectpoints[1]),tuple(rectpoints[2]),rectcolor,2)
            line(img,tuple(rectpoints[2]),tuple(rectpoints[3]),rectcolor,2)
            line(img,tuple(rectpoints[3]),tuple(rectpoints[0]),rectcolor,2)
            imshow("detectedimage",img)
            #imshow("plate",plates[i].Plate)
            temp = 'C:\\Users\\home\\Desktop\\project\\Cropped_Image\\'
            imwrite(temp+"plate.png",plates[i].Plate)
    waitKey(0)
