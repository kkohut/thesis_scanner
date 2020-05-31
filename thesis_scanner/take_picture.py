"""
WORK IN PROGRESS
This script is used to open the webcam and take pictures by pressing space
It can be exited by pressing Esc
Needed to acces the camera and then take a picture of the thesis, so it can be processed afterwards
by Daniel Rindin
"""

import cv2 #using opencv version 4.2.0 for python 3.8
from timer import Timer

#Settings ( can be changed individually )
width = 1080
height = 720        
timeout_limit = 30  #in seconds
used_camera = 0     #use default camera using default backend
#

t = Timer()

def initialize_camera(width ,height):
    #creates object using the first camera listed (0)
    cam = cv2.VideoCapture(used_camera)
    #set Resolution
    cam.set(3,width)
    cam.set(4,height)
    return cam

def keep_picture(frame):
    """
    After the camera is initialized and a picture is taken, the function shows the taken picture.
    It can be decided whether the picture is kept by pressing 's' -> the picture will be saved
    Or take a new picture by pressing 'ESC' 
    """
    t.start()
    while t.elapsed_time() < timeout_limit:
        cv2.imshow('image',frame)
        t.print_elapsed_time()
        k = cv2.waitKey(1)
        if k%256 == 27:         # wait for ESC key to exit
            cv2.destroyWindow("image")
            break
        elif k%256 == ord('s'): # press "S" to save the picture and exit
            t.stop()
            img_name = "thesis.jpg"
            #saves the image
            cv2.imwrite(img_name, frame)
            img = cv2.imread(img_name)
            print("{} saved!".format(img_name))
            cv2.destroyAllWindows()
            return img
    t.stop()

def process():
    print("starting...")
    img = None
    cam = initialize_camera(width,height) 
    cv2.namedWindow("test")     #creates new window called "test"
    
    t.start() 

    while t.elapsed_time() < timeout_limit:
        #reads the input from the camera and shows it in the window "test"
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        
        t.print_elapsed_time()
        #add Timeout!

        k = cv2.waitKey(1)  #waits for a key to be pressed

        if k%256 == 27: # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:   #Space pressed
            t.stop()
            img = keep_picture(frame)
            t.start()
            if img is not None:
                break

    t.stop()
    cam.release()

    cv2.destroyAllWindows()
    if img is not None:
        return img


img = process()
"""
#process will return the taken image; the following code shows the taken picture from the process
if img is not None:
    cv2.imshow("test",img)
    cv2.waitKey(0)  #close window by pressing any key
    cv2.destroyAllWindows()
else:
    print("no picture taken")
"""