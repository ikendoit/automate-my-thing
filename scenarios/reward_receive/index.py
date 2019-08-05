#!/usr/bin/env python3 

import numpy as np
import imutils
from mss import mss
from PIL import Image
import cv2
import time
import pyautogui as pag
import os
import sys
from utils import *

ASSETS_REWARDER             = cv2.imread("./assets/rewarder.png");
ASSETS_PET_YARD             = cv2.imread("./assets/pet-yard.png");
ASSETS_ENTER_REWARDER       = cv2.imread("./assets/enter-rewarder.png");
ASSETS_LOGIN_SEER_NPC       = cv2.imread("./assets/login-seer-npc.png");
ASSETS_LOGIN_SEER_BUTTON    = cv2.imread("./assets/login-seer-button.png");
ASSETS_LOGIN_PANEL_TITLE    = cv2.imread("./assets/login-reward-title.png");
ASSETS_EXIT_LOGIN_PANEL     = cv2.imread("./assets/exit-login-reward.png");
current_goal = 'EXIT_ADS' # EXIT_ADS, PET_YARD, REWARDER, REWARDER_BUTTON, GO_TO_LOGIN_SEER, LOGIN_SEER_BUTTON

IS_DEBUG = os.getenv('DEBUG') == 'TRUE' 
IS_DEBUG and print("DEBUG MODE>>>>")
#current_goal = 'GO_TO_LOGIN_SEER' if IS_DEBUG else current_goal 

def moveToPetYard(cv2, screen):
    IS_DEBUG and print("to pet yard")
    return moveToObject(cv2, screen, ASSETS_PET_YARD, 100, +210)

def moveToRewarder(cv2, screen):
    IS_DEBUG and print("to rewarder")
    return moveToObject(cv2, screen, ASSETS_REWARDER, 20, 25);

def accessRewardRoom(cv2, screen):
    target_object = getCoordTemplate(cv2, ASSETS_ENTER_REWARDER, screen)
    if target_object is None:
        print("Cannot find access rewarder button");
        pag.click(x=config.SCREEN_LEFT_PADDING+target_object[1]+70, y=config.SCREEN_TOP_PADDING+target_object[0]+55);
        return False
    pag.click(x=config.SCREEN_LEFT_PADDING+target_object[1]+70, y=config.SCREEN_TOP_PADDING+target_object[0]+55);
    return True;

def moveToLoginSeer(cv2, screen):
    keyPress("w")
    keyPress("a")
    login_reward_button = getCoordTemplate(cv2, ASSETS_LOGIN_SEER_BUTTON, screen, 0.8)
    return login_reward_button is not None;

def accessLoginPanel(cv2, screen):
    target_object = getCoordTemplate(cv2, ASSETS_LOGIN_SEER_BUTTON, screen, 0.8)
    if target_object is None:
        keyPress("w")
        return False;
    pag.click(x=config.SCREEN_LEFT_PADDING+target_object[1]+70, y=config.SCREEN_TOP_PADDING+target_object[0]+65);
    return True;


def access_calendar_from_home(screen, cv2):
    global current_goal;

    if current_goal == 'EXIT_ADS':
        # focus on game
        pag.doubleClick(x=720+config.SCREEN_LEFT_PADDING, y=config.SCREEN_TOP_PADDING + 25)
        pag.doubleClick(x=720+config.SCREEN_LEFT_PADDING, y=config.SCREEN_TOP_PADDING + 25)

        # exit ads by double tap 'o', only happens once
        keyPress('o')
        time.sleep(2)
        keyPress('o')

        # re-set orientation to look straight north
        keyPress('z')
        keyPress('z')

        current_goal = "PET_YARD"

    if current_goal == 'PET_YARD' and moveToPetYard(cv2, screen):
        current_goal = 'REWARDER'

    if current_goal == 'REWARDER' and moveToRewarder(cv2, screen):
        current_goal = 'REWARDER_BUTTON'

    if current_goal == 'REWARDER_BUTTON' and accessRewardRoom(cv2, screen):
        current_goal = 'GO_TO_LOGIN_SEER'

    if current_goal == 'GO_TO_LOGIN_SEER' and moveToLoginSeer(cv2, screen):
        current_goal = 'LOGIN_SEER_BUTTON'

    if current_goal == 'LOGIN_SEER_BUTTON' and accessLoginPanel(cv2, screen):
        IS_DEBUG and print("accessing the reward calendar panel")
        time.sleep(2)
        select_calendar_dates(screen, cv2)

def select_calendar_dates(screen, cv2):

    screen = grabScreenImage();
    login_reward_title    = getCoordTemplate(cv2, ASSETS_LOGIN_PANEL_TITLE, screen, 0.6)
    if login_reward_title is None:  
        print("Could not detect login reward title from module")
        return;

    (y, x) = login_reward_title

    pag.PAUSE = 0.1
    for i in range(1, 8):
        for j in range(1, 6):
            mouse_coord_x = config.SCREEN_LEFT_PADDING+x+i*80
            mouse_coord_y = config.SCREEN_TOP_PADDING+y+j*80 + 80
            pag.doubleClick(x= mouse_coord_x, y = mouse_coord_y )
            pag.doubleClick(x= mouse_coord_x, y = mouse_coord_y )
    pag.PAUSE = 0

    IS_DEBUG and print("done, exiting...");
    exit_button = getCoordTemplate(cv2, ASSETS_EXIT_LOGIN_PANEL, screen, 0.8)
    if exit_button is None:
        print("cannot see exit button for reward panel")
        return;
    pag.doubleClick(x=config.SCREEN_LEFT_PADDING+exit_button[1]+65, y = config.SCREEN_TOP_PADDING+exit_button[0]+5)

    exitTab()
    sys.exit(0)
