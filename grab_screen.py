#!/usr/bin/env python3 

import traceback
import numpy as np
import imutils
import time
import pyautogui as pag
from utils import *
from scenarios.reward_receive.index import access_calendar_from_home
from scenarios.fight.index import go_to_fight_from_home
import cv2
import config
import sys


IS_DEBUG = os.getenv('DEBUG') == 'TRUE' 
AUTO_MODE = 'LOGIN' if os.getenv('MODE') is None else os.getenv('MODE').upper()
ASSETS_SERVER_MENU_OPTION   = cv2.imread("./assets/server-menu.png");
ASSETS_MAIN_MENU_OPTION     = cv2.imread("./assets/main-menu-button.png");
ASSETS_USER_PROFILE_BAR     = cv2.imread("./assets/map-home-menu.png");

WINDOW_NAME='wind1'
IS_DEBUG and cv2.namedWindow(WINDOW_NAME)
IS_DEBUG and cv2.moveWindow(WINDOW_NAME, 20, 20)

currentMode = None # MAP_SELECTION; GAME_HOME; CHAR_SELECTION; 
def detectMode(image):

    global currentMode;
    isIntroMenu             = None
    isCharSelection         = None
    isAtUserProfileBar      = None

    # To reduce the amount of template matching every frame
    #   we will detect mode once, and start logically follow the flow of actions
    if currentMode is None or currentMode != "GAME_HOME":
        isIntroMenu             = getCoordTemplate(cv2, ASSETS_SERVER_MENU_OPTION, image)
        isCharSelection         = getCoordTemplate(cv2, ASSETS_MAIN_MENU_OPTION, image)
        isAtUserProfileBar      = getCoordTemplate(cv2, ASSETS_USER_PROFILE_BAR, image, 0.8)

    if isIntroMenu is not None:
        pag.click(x=config.SCREEN_LEFT_PADDING+isIntroMenu[1]+140, y=config.SCREEN_TOP_PADDING+isIntroMenu[0] + 20)
        currentMode = "CHAR_SELECTION"
        return;

    if currentMode == "CHAR_SELECTION" and isCharSelection is not None:
        pag.click(x=config.SCREEN_LEFT_PADDING+isCharSelection[1]+140, y=config.SCREEN_TOP_PADDING+isCharSelection[0] + 20)
        currentMode == "GAME_HOME"
        return;

    if AUTO_MODE == 'LOGIN' and (currentMode == "GAME_HOME" or isAtUserProfileBar is not None):
        access_calendar_from_home(image, cv2)
        currentMode == "GAME_HOME" # Could also change AUTO_MODE to "FIGHT_MODE"
        return;

    if AUTO_MODE == 'FIGHT' and (currentMode == "GAME_HOME" or isAtUserProfileBar is not None):
        go_to_fight_from_home(image, cv2)
        currentMode == "GAME_HOME" # or FIGHT_MODE
        return;

    print("not sure where we are in main :(");
    time.sleep(1.8)

def mss_grab_screen():

    try:
        # focus on game
        pag.doubleClick(x=720+config.SCREEN_LEFT_PADDING, y=config.SCREEN_TOP_PADDING + 25)
        pag.doubleClick(x=720+config.SCREEN_LEFT_PADDING, y=config.SCREEN_TOP_PADDING + 25)

        # exit ads by double tap 'o', only happens once
        #keyPress('o')
        #time.sleep(2)
        #keyPress('o')

        # re-set orientation to look straight north
        keyPress('z')
        keyPress('z')

        while(True):

            image = grabScreenImage();
            detectMode(image);

            IS_DEBUG and highlightInImage(image, 420, 275)
            IS_DEBUG and cv2.imshow(WINDOW_NAME, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if cv2.waitKey(15) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    except Exception as e:
        print('exiting... closing display', e)
        cv2.destroyAllWindows()
        traceback.print_exc()

mss_grab_screen()
