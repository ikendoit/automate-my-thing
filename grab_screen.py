#!/usr/bin/env python3 

import numpy as np
import imutils
import pyautogui as pag
from utils import *
import cv2

WINDOW_NAME='wind1'
cv2.namedWindow(WINDOW_NAME)
cv2.moveWindow(WINDOW_NAME, 20, 20)


#assets_play_button          = cv2.imread("./assets/play-button.png");
# import game map assets, fight screen asset for detection

def mss_grab_screen():

    try:

        # focus on game
        pag.click(x=410+2200, y=550)
        while(True):

            image = grabScreenImage();
            highlightInImage(image, 420, 275)
            cv2.imshow(WINDOW_NAME, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # exit signal
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


    except Exception as e:
        print('exiting... closing display', e)
        cv2.destroyAllWindows()

mss_grab_screen()
