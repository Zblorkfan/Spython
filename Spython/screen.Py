
import cv2
import numpy as np
import pyautogui
import time
import pygame
def watch_screen(): 
    SCREEN_SIZE = (1920, 1080)
    fource = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fource, 20.0, (SCREEN_SIZE))

    fps =30
    prev = 0
    pygame.init()
    tpsz = pygame.time.get_ticks()

    while True:
        if pygame.time.get_ticks() - tpsz  > 10000: 
            break
        time_elapsed = time.time()-prev
        img = pyautogui.screenshot()
        if time_elapsed > 1.0/fps:
            prev = time.time()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
