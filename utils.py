#!/usr/bin/env python3 
import numpy as np
import imutils
import pyautogui as pag
from mss import mss
from PIL import Image
import os
import config

IS_DEBUG = os.getenv('DEBUG') == 'TRUE' 
sct = mss()
monitorSelection = sct.monitors[1]
monitorFormat = {"top": config.SCREEN_TOP_PADDING, "left": config.SCREEN_LEFT_PADDING, "width": config.CANVAS_WIDTH, "height": config.CANVAS_HEIGHT}
THRESHOLD_MATCH_TEMPLATE = 0.6;

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
                  

""" New Section
                                                         __                         
                                                        /  |                        
      ______    ______    ______   _____  ____    ______   _$$ |_     ______   __    __ 
     /      \  /      \  /      \ /     \/    \  /      \ / $$   |   /      \ /  |  /  |
    /$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |/$$$$$$  |$$$$$$/   /$$$$$$  |$$ |  $$ |
    $$ |  $$ |$$    $$ |$$ |  $$ |$$ | $$ | $$ |$$    $$ |  $$ | __ $$ |  $$/ $$ |  $$ |
    $$ \__$$ |$$$$$$$$/ $$ \__$$ |$$ | $$ | $$ |$$$$$$$$/   $$ |/  |$$ |      $$ \__$$ |
    $$    $$ |$$       |$$    $$/ $$ | $$ | $$ |$$       |  $$  $$/ $$ |      $$    $$ |
     $$$$$$$ | $$$$$$$/  $$$$$$/  $$/  $$/  $$/  $$$$$$$/    $$$$/  $$/        $$$$$$$ |
    /  \__$$ |                                                                /  \__$$ |
    $$    $$/                                                                 $$    $$/ 
     $$$$$$/                                                                   $$$$$$/  
"""
# @param: target img; screen img
# return (y,x) / None coord of top-left where they match
def getCoordTemplate(cv2, target, screen, match_threshold=THRESHOLD_MATCH_TEMPLATE):
    result = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
    coord = np.where(result > THRESHOLD_MATCH_TEMPLATE);
    if len(coord[0]) == 0:
        return None;
    return (coord[0][0], coord[1][0]);

def grabScreenImage():
    sct_img = sct.grab(monitorFormat)
    image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    return np.array(image);

# highlight in image from np.array()
def highlightInImage(img, ycoord, xcoord):
    for i in range(ycoord , ycoord+60):
        for j in range(xcoord , xcoord+50):
            img[i][j] = np.array([255,255,255])

""" New Section
     __                            __                                            __ 
    |  \                          |  \                                          |  \
    | $$   __   ______   __    __ | $$____    ______    ______    ______    ____| $$
    | $$  /  \ /      \ |  \  |  \| $$    \  /      \  |      \  /      \  /      $$
    | $$_/  $$|  $$$$$$\| $$  | $$| $$$$$$$\|  $$$$$$\  \$$$$$$\|  $$$$$$\|  $$$$$$$
    | $$   $$ | $$    $$| $$  | $$| $$  | $$| $$  | $$ /      $$| $$   \$$| $$  | $$
    | $$$$$$\ | $$$$$$$$| $$__/ $$| $$__/ $$| $$__/ $$|  $$$$$$$| $$      | $$__| $$
    | $$  \$$\ \$$     \ \$$    $$| $$    $$ \$$    $$ \$$    $$| $$       \$$    $$
     \$$   \$$  \$$$$$$$ _\$$$$$$$ \$$$$$$$   \$$$$$$   \$$$$$$$ \$$        \$$$$$$$
                        |  \__| $$                                                  
                         \$$    $$                                                  
                          \$$$$$$                                                   
"""

def keyPress(key, times=1):
    for i in range(0,times):
        pag.keyDown(key);
        pag.keyUp(key);

"""
    ________________-> (Ox) array-index 1
    |...............                    
    |..........#....     
    |...............    
    |...............    
    |.......*.......    
    |...............    
    v                   
   (Oy)
  array-index 0

"""
# target, char: [y][x] coordinates
# return: boolean: are we there yet ?
def positionToObject(target, char):
    # character is <position> to the target
    tooLow   =  char[0] > target[0] + 50
    tooHigh  =  char[0] < target[0] - 50
    tooRight =  char[1] > target[1] + 50
    tooLeft  =  char[1] < target[1] - 50

    if tooRight:
        keyPress('a') # increase target[1] ( x coor )

    if tooLeft:
        keyPress('d') # decrease target[1] ( x coor )

    if tooLow: 
        keyPress('w') # increase target[0] ( y coor )

    if tooHigh:
        keyPress('s') # decrease target[0] ( y coor )

    if not tooLow and not tooLeft and not tooRight and not tooHigh:
        return True;
    else:
        return False

def moveToObject(cv2, screen, image_object, offSetY=0, offSetX=0, threshold=0.6):    
    target_object = getCoordTemplate(cv2, image_object, screen, threshold)
    if target_object is None:
        print("not sure what im doing")
        keyPress('w')
        return False;
    IS_DEBUG and highlightInImage(screen, target_object[0], target_object[1])

    return positionToObject((target_object[0]+offSetY, target_object[1]+offSetX), (445, 300))
