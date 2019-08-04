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
    target_object = getCoordTemplate(image_object, printscreen)
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
    target_object = getCoordTemplate(image_object, printscreen)
    for i in range(target_object[0]+10,target_object[0]+10):
        for j in range(target_object[1]+18,target_object[1]+5):
            printscreen[i][j] = np.array([255,255,255])

    pag.click(x=2200+target_object[1]+70, y=200+target_object[0]+55);
    return True;



def run(screen, cv2):
    global current_goal;

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


