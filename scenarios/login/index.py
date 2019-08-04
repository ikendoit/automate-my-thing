#!/usr/bin/env python3 

import numpy as np
import imutils
from mss import mss
from PIL import Image
import cv2
import time
import pyautogui as pag
from utils import *

ASSETS_PLAY_BUTTON          = cv2.imread("./assets/play-button.png");
ASSETS_PET_YARD             = cv2.imread("./assets/pet-yard.png");
ASSETS_BARBARIAN            = cv2.imread("./assets/barbarian.png");
ASSETS_ENTER_REWARDER       = cv2.imread("./assets/enter-rewarder.png");


def run(screen, cv2, sct):
    print("asdf")
