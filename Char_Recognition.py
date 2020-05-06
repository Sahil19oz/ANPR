from PIL import Image
from pytesseract import image_to_string
import time

def OCR(path):
    inputt=Image.open(path)
    output=image_to_string(inputt,lang='eng')
    return(output)
