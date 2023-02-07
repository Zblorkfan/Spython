import cv2
import pygame


def use_webcam(): 
    vid_capture = cv2.VideoCapture(0)
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter("cam_video.avi", vid_cod, 20.0, (640,480))
    pygame.init()
    tps = pygame.time.get_ticks()
    while(True):
         # Capture each frame of webcam video
   
         ret,frame = vid_capture.read()
         output.write(frame)
         # Close and break the loop after pressing "x" key
         if (pygame.time.get_ticks() - tps)/1000 > 10:
             break


    # close the already opened camera
    vid_capture.release()
    # close the already opened file
    output.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()






