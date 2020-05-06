import math
import cv2

class ifChar:
    def __init__(self, cntr):
        self.contour = cntr
        self.boundingRect = cv2.boundingRect(self.contour)
        [x, y, w, h] = self.boundingRect
        self.boundingRectX = x
        self.boundingRectY = y
        self.boundingRectWidth = w
        self.boundingRectHeight = h
        self.boundingRectArea = self.boundingRectWidth * self.boundingRectHeight
        self.centerX = (self.boundingRectX + self.boundingRectX + self.boundingRectWidth) / 2
        self.centerY = (self.boundingRectY + self.boundingRectY + self.boundingRectHeight) / 2
        self.diagonalSize = math.sqrt((self.boundingRectWidth ** 2) + (self.boundingRectHeight ** 2))
        self.aspectRatio = float(self.boundingRectWidth) / float(self.boundingRectHeight)


class PossiblePlate:
    def __init__(self):
        self.Plate = None
        self.Grayscale = None
        self.Thresh = None
        self.rrLocationOfPlateInScene = None
        self.strChars = ""


def checkIfChar(possibleChar):
    if (possibleChar.boundingRectArea > 80 and possibleChar.boundingRectWidth > 2 and possibleChar.boundingRectHeight > 8 and 0.25 < possibleChar.aspectRatio < 1.0):
        return True
    else:
        return False


# check the center distance between characters
def distanceBetweenChars(firstChar, secondChar):
    x = abs(firstChar.centerX - secondChar.centerX)
    y = abs(firstChar.centerY - secondChar.centerY)
    return math.sqrt((x ** 2) + (y ** 2))


# use basic trigonometry (SOH CAH TOA) to calculate angle between chars
def angleBetweenChars(firstChar, secondChar):
    adjacent = float(abs(firstChar.centerX - secondChar.centerX))
    opposite = float(abs(firstChar.centerY - secondChar.centerY))
    if adjacent != 0.0:
        angleInRad = math.atan(opposite / adjacent)
    else:
        angleInRad = 1.5708
    angleInDeg = angleInRad * (180.0 / math.pi)
    return angleInDeg
