#!/bin/python

import cv2
import os
import time
import sys
import select

merge_ratio = 0.75
merge_inc = 0.05

cam = cv2.VideoCapture("/dev/video0")

def genoverlay(fg, bg, ratio):
    if fg is None or bg is None:
        return None

    return cv2.addWeighted(fg, ratio, bg, 1.0-ratio, 0)

fg = None
bg = None
while True:
    choice = cv2.waitKey(50)
    if choice != -1:
        choice = chr(choice & 0x7f)

    # Store background pic
    if choice == 'b':

        ret, frame = cam.read()

        if ret:
            bg = frame
            #cv2.imshow('bg', bg)
        else:
            print('Failed to take screenshot')

        continue

    # Adjust up background/foreground image merge ratio
    elif choice == 'k':
        merge_ratio += merge_inc
        if merge_ratio > 1.0:
            merge_raio = 1.0

        continue

    # Adjust down background/foreground image merge ratio
    elif choice == 'j':
        merge_ratio -= merge_inc
        if merge_ratio < 0.0:
            merge_ratio = 0.0

        continue

    # Exit
    elif choice == 'q' or choice == 'x':
        break

    # Render resulting image
    else:

        ret, frame = cam.read()

        if ret:
            fg = frame
            overlay = genoverlay(fg, bg, merge_ratio)
            if not overlay is None:
                cv2.imshow('overlay', overlay)
            else:
                cv2.imshow('overlay', fg)

        else:
            print('Failed to render overlay')

cam.release()
cv2.destroyAllWindows()
