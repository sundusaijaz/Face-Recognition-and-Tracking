from time import time
import cv2
from faceDetector import face_detector

import os

username = input("Enter Name:")
current_directory = os. getcwd()+'\\faces\\'

face_detector = face_detector.FaceDetection()


def startCapture():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Face Capture")

    img_counter = 0
    width = 400
    height = 400
    dim = (width, height)
    while True:
        ret, frame = cam.read()
        if not ret:
            
            print("failed to grab frame")
            break
        frame,top,left,top_height,left_width = face_detector(frame=frame)
        cropped_image = frame[int(top):int(top_height),int(left):int(left_width),:]
        resized_image = cv2.resize(cropped_image,dim)
        

        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = username+".png"
            cv2.imwrite(img_name, resized_image)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

cv2.destroyAllWindows()


startCapture()