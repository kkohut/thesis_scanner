"""
WORK IN PROGRESS
This script is used to open the webcam and take pictures by pressing space
It can be exited by pressing Esc
Needed to acces the camera and then take a picture of the thesis, so it can be processed afterwards
by Daniel Rindin
"""

import cv2 #using opencv version 4.2.0 for python 3.8

def initialize_camera(width ,height):
    #creates object using the first camera listed (0)
    cam = cv2.VideoCapture(0)
    #set Resolution
    cam.set(3,width)
    cam.set(4,height)
    return cam

def process():
    print("starting...")

    cam = initialize_camera(1080,720)

    #creates new window called "test"
    cv2.namedWindow("test")
    #img counter if more than one pictures are taken
    img_counter = 0

    while True:
        #reads the input from the camera and shows it in the window "test"
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break

        #waits for a key to be pressed
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            cv2.imshow('image',frame)
            k = cv2.waitKey(0)
            if k%256 == 27:         # wait for ESC key to exit
                cv2.destroyWindow("image")
            elif k%256 == ord('s'): # wait for 's' key to save and exit
                img_name = "opencv_frame_{}.png".format(img_counter)
                #saves the image
                cv2.imwrite(img_name, frame)
                cv2.destroyAllWindows()
            print("{} saved!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()

process()