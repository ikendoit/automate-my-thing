#!/usr/bin/env python3 

import numpy as np
import imutils
from mss import mss
from PIL import Image
import cv2
import time
import pyautogui as pag
from utils import *

ASSETS_REWARDER             = cv2.imread("./assets/rewarder.png");
ASSETS_PET_YARD             = cv2.imread("./assets/pet-yard.png");
ASSETS_BARBARIAN            = cv2.imread("./assets/barbarian.png");
ASSETS_ENTER_REWARDER       = cv2.imread("./assets/enter-rewarder.png");
current_goal = 'PET_YARD' # PET_YARD, BARBARIAN, REWARDER, REWARDER_ENTER

WINDOW_NAME='wind1'
cv2.namedWindow(WINDOW_NAME)
cv2.moveWindow(WINDOW_NAME, 20, 20)

def keyPress(key):
    print('press', key);
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
    print(target, char)
    tooLow   =  char[0] > target[0] + 60
    tooHigh  =  char[0] < target[0] 
    tooRight =  char[1] > target[1] + 60
    tooLeft  =  char[1] < target[1]

    if tooLow: 
        keyPress('w') # increase target[0] ( y coor )

    if tooHigh:
        keyPress('s') # decrease target[0] ( y coor )

    if tooRight:
        keyPress('a') # increase target[1] ( x coor )

    if tooLeft:
        keyPress('d') # decrease target[1] ( x coor )

    if not tooLow and not tooLeft and not tooRight and not tooHigh:
        return True;
    else:
        return False

def moveToObject(printscreen, image_object):    
    # highlight pet yard
    target_object = getCoordTemplate(cv2, image_object, printscreen)
    if target_object is None:
        return False;
    for i in range(target_object[0],target_object[0]+40):
        for j in range(target_object[1],target_object[1]+40):
            printscreen[i][j] = np.array([255,255,255])

    return positionToObject(target_object, (445, 300))

def moveToPetYard(printscreen):
    return moveToObject(printscreen, ASSETS_PET_YARD);

def moveToBarbarian(printscreen):
    return moveToObject(printscreen, ASSETS_BARBARIAN);

def moveToRewarder(printscreen):
    return moveToObject(printscreen, ASSETS_REWARDER);

def accessRewardRoom(printscreen):
    target_object = getCoordTemplate(cv2, image_object, printscreen)
    if target_object is None:
        return False
    for i in range(target_object[0]+10,target_object[0]+10):
        for j in range(target_object[1]+18,target_object[1]+5):
            printscreen[i][j] = np.array([255,255,255])

    pag.click(x=2200+target_object[1]+70, y=200+target_object[0]+55);
    return True;

def mss_grab_screen():
    global current_goal;
    sct = mss()
    still_image = None
    pag.click(x=410+2200, y=550)

    while(True):

        # get image
        monitorSelection = sct.monitors[1]
        monitorFormat = {"top": 200, "left": 2200, "width": 805, "height": 630}
        sct_img = sct.grab(monitorFormat)
        image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

        # PARSE IMAGE
        printscreen = np.array(image)
        # highlight user
        for i in range(420,470):
            for j in range(275, 325):
                printscreen[i][j] = np.array([0,0,0])

        if current_goal == 'PET_YARD' and moveToPetYard(printscreen):
            print("going to barbara")
            current_goal = 'BARBARIAN'

        if current_goal == 'BARBARIAN' and moveToBarbarian(printscreen):
            print("going to rewarder")
            current_goal = 'REWARDER'

        if current_goal == 'REWARDER' and moveToRewarder(printscreen):
            current_goal = 'REWARDER_BUTTON'

        if current_goal == 'REWARDER_BUTTON' and accessRewardRoom(printscreen):
            print("we are there");

        # convert img to grayscale, and blur it
        #gray = cv2.cvtColor(np.float32(image), cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # highlight moving objects on screen
        #if still_image is not None:
        #    diff = np.normalize(gray - still_image);
        #    #diff = cv2.absdiff(still_image, gray);
        #    #getLongestLineNon0(diff)
        # capture still image motion
        #if still_image is None or cv2.waitKey(25) & 0xFF == 32:
        #    print(cv2.waitKey(23) & 0xFF)
        #    print("CAPTURE STILL IMAGE")
        #    still_image = gray


        # PRINT IMAGE
        cv2.imshow(WINDOW_NAME, cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))

        # exit signal
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

mss_grab_screen()
