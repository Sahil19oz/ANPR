import cv2
import os
import numpy as np
import math
import argparse
from time import time
from preprocess import PROCESSING
from PlateDetector import POSSIBLEPLATES
from Char_Recognition import OCR
from PlateProcess import plateprocessing

arg=argparse.ArgumentParser()
arg.add_argument("-i","--image",type=str,required=True,help="Image Path")
args=vars(arg.parse_args())


path=(args["image"])
temp=os.getcwd()
#Calling processing function to preprocess the input image
starttime=time()
height,width,contours=PROCESSING(os.path.join(temp,"test_data",path))
POSSIBLEPLATES(path,height,width,contours)
#ocr_output=plateprocessing()
ocr_output=OCR(os.path.join(temp,"test_data",path))

print("PLATE NUMBER DETECTED IS:- {}".format(ocr_output))
print("TOTAL PROCESSING TIME IS:- {}".format(time()-starttime))
