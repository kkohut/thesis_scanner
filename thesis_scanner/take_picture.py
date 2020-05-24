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

def keep_picture(frame, img_counter):
    """
    After the camera is initialized and a picture is taken, the function shows the taken picture.
    It can be decided whether the picture is kept by pressing 's' -> the picture will be saved
    Or take a new picture by pressing 'ESC' 
    """
    cv2.imshow('image',frame)
    k = cv2.waitKey(0)
    if k%256 == 27:         # wait for ESC key to exit
        cv2.destroyWindow("image")
    elif k%256 == ord('s'): # press "S" to save the picture and exit
            img_name = "thesis{}.png".format(img_counter)
            #saves the image
            cv2.imwrite(img_name, frame)
            img = cv2.imread(img_name)
            print("{} saved!".format(img_name))
            img_counter += 1
            cv2.destroyAllWindows()
            return img


def process():
    print("starting...")
    img = None
    cam = initialize_camera(1080,720)
    cv2.namedWindow("test")     #creates new window called "test"
    img_counter = 0     #img counter if more than one pictures are taken

    while True:
        #reads the input from the camera and shows it in the window "test"
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break

        k = cv2.waitKey(1)  #waits for a key to be pressed

        if k%256 == 27: # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:   #Space pressed
            img = keep_picture(frame,img_counter)
            if img is not None:
                break

    cam.release()

    cv2.destroyAllWindows()
    if img is not None:
        return img

img = process()
#process will return the taken image; the following code shows the taken picture from the process
if img is not None:
    cv2.imshow("test",img)
    cv2.waitKey(0)  #close window by pressing any key
    cv2.destroyAllWindows()
else:
    print("no picture taken")