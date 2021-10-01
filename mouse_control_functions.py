import time

import lackey
import pyautogui
from lackey import *




# def mouse_move(x, y):
#     hover(Location(100,200))

def mouse_move(x, y, t=1):
    pyautogui.moveTo(x, y, t)
    time.sleep(0.1)


def mouse_move_click(x, y, t=1):
    pyautogui.moveTo(x, y, t)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)


def mouse_move_click_left(x, y, t=1):
    pyautogui.dragTo(x, y, t, button='left')


def mouse_click(*kords):
    time.sleep(0.1)
    if kords:
        pyautogui.click(kords[0], kords[1])
    else:
        pyautogui.click()
    time.sleep(0.1)


def mouse_click_and_move(x, y, t=1):
    time.sleep(0.1)
    pyautogui.dragTo(x, y, t, button='left')
    time.sleep(0.1)

