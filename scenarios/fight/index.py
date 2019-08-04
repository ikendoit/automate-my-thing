#!/usr/bin/env python3 

import numpy as np
from mss import mss
import cv2
import time
import pyautogui as pag
from utils import *
import os
IS_DEBUG = os.getenv('DEBUG') == 'TRUE' 

ASSETS_FIGHT_GATEWAY        = cv2.imread("./assets/fight-gateway.png")
ASSETS_FIGHT_ENTER_BUTTON   = cv2.imread("./assets/fight-enter-button.png")
current_goal = None;

def moveToFightGateway(cv2, screen):
    return moveToObject(cv2, screen, ASSETS_FIGHT_GATEWAY, 50, 50, 0.9)

def accessFightGateway(cv2, screen):
    enter_button = getCoordTemplate(cv2, ASSETS_FIGHT_ENTER_BUTTON, screen)
    if enter_button is not None:    
        pag.doubleClick(x=2220+enter_button[1]+80, y=200+enter_button[0]+40)  
        return True;
    return False;   

def go_to_fight_from_home(screen, cv2):
    global current_goal;

    if current_goal is None and moveToFightGateway(cv2, screen):
        current_goal = "FIGHT"

    if current_goal == 'FIGHT' and accessFightGateway(cv2, screen):
        print("Should be at enter button")
