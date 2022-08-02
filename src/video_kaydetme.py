import numpy as np
import cv2

def video_record():
    
    sayac = 0
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('output/webcam.mp4',fourcc, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            sayac+=1
            frame = cv2.flip(frame,1)
            out.write(frame)

            if sayac>=200:
                break
        else:
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()