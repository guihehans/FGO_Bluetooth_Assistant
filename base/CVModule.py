import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api
import sys


class CVModule:
    pass


if __name__ == '__main__':
    # Load an color image in grayscale
    path = r'..\Template\Add_friend.jpg'
    img = cv.imread(path, 0)
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
