#!/usr/bin/env python3 
import numpy as np
import imutils
import pyautogui as pag
from mss import mss
from PIL import Image

sct = mss()
monitorSelection = sct.monitors[1]
monitorFormat = {"top": 200, "left": 2200, "width": 805, "height": 630}
THRESHOLD_MATCH_TEMPLATE = 0.8;

# receive the "cv2.absdiff" between 2 images in float[]
#   return the middlepoint of the longest pixel line (horizontally) in array
def getLongestLineNon0(diff):
    #thresh = cv2.threshold(diff, 0, 255,
    #        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #        cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    #print(cnts);
    blackPixel          = 0.
    maxLength           = 0;
    firstPoint          = None;
    mainCenterRow       = 0;
    mainCenterColumn    = 0;
    for rowIndex, row in enumerate(diff):

        currentLength = 0;

        for columnIndex, pixel in enumerate(row):   
            # start recording horizontal, differentiable line
            if pixel != blackPixel:  
                if firstPoint is None:
                    firstPoint = pixel;
                currentLength = currentLength + 1;
            # end recording horizontal, differentiable line
            else:
                if firstPoint is None:
                    continue;
                if currentLength > maxLength:
                    mainCenterRow    = rowIndex
                    maincenterColumn = columnIndex
                    maxLength = currentLength;
                firstPoint = None;
    print(mainCenterRow, mainCenterColumn);
                  

# @param: target img; screen img
# return (y,x) / None coord of top-left where they match
def getCoordTemplate(cv2, target, screen):
    result = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
    coord = np.where(result > THRESHOLD_MATCH_TEMPLATE);
    if len(coord[0]) == 0:
        return None;
    return (coord[0][0], coord[1][0]);

def keyPress(key):
    print('press', key);
    pag.keyDown(key);
    pag.keyUp(key);


def grabScreenImage():
    sct_img = sct.grab(monitorFormat)
    image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    return np.array(image);

# highlight in image from np.array()
def highlightInImage(img, ycoord, xcoord):
    for i in range(ycoord , ycoord+60):
        for j in range(xcoord , xcoord+50):
            img[i][j] = np.array([0,0,0])
