"""
this script is a unittest script to the "take_picture.py" script 
by Daniel Rindin
"""

import cv2
import take_picture , unittest
import numpy    #needed to create empty image 

import threading
from pynput.keyboard import Key, Controller
import time
import os

keyboard = Controller()

class TestTake_PictureMethods(unittest.TestCase):
    
    def test_initialize_camera(self):
        camNr = 0   #use default camera

        cam = take_picture.initialize_camera(camNr)
        self.assertTrue(cam.read()[camNr])  #cam.read()[camNr] == True if cam is connected
        cam.release()

    def test_keep_picture_saved(self):
        removeFile()

        thread1 = Thread_Keep_Picture()
        thread2 = Thread_Key_Press('s',0)

        thread1.start()
        waitForWindow('image')
        thread2.start()

        thread1.join()
        thread2.join()

        self.assertTrue(os.path.isfile("./thesis.jpg"))
        os.remove("./thesis.jpg")

    def test_keep_picture_canceled(self):
        removeFile()

        thread1 = Thread_Keep_Picture()
        thread2 = Thread_Key_Press(Key.esc,0) 

        thread1.start()
        waitForWindow('image')
        thread2.start()

        thread1.join()
        thread2.join()

        self.assertFalse(os.path.isfile("./thesis.jpg"))

    def test_keep_picture_timeout(self):
        removeFile()
        blank_image = numpy.zeros(shape=[512, 512, 3], dtype=numpy.uint8)
        take_picture.keep_picture(blank_image,3)
        #keep_picture does nothing -> waits for timeout after 3sec
        self.assertFalse(os.path.isfile("./thesis.jpg"))
    
    def test_show_cam_take_picture(self):
        removeFile()

        thread1 = Thread_Show_Cam()
        thread2 = Thread_Key_Press(Key.space,0) 
        thread3 = Thread_Key_Press('s',1)

        thread1.start()
        waitForWindow('Thesis Scanner')
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()
 
        self.assertTrue(os.path.isfile("./thesis.jpg"))
        os.remove("./thesis.jpg")

    def test_show_cam_canceled(self):
        removeFile()

        thread1 = Thread_Show_Cam()
        thread2 = Thread_Key_Press(Key.esc,0) 
        
        thread1.start()
        waitForWindow('Thesis Scanner')
        thread2.start()

        thread1.join()
        thread2.join()

        self.assertFalse(os.path.isfile("./thesis.jpg"))

    def test_show_cam_timeout(self):
        removeFile()
        cam = take_picture.initialize_camera(0)
        take_picture.show_cam(cam,3)
        #show_cam does nothing -> waits for timeout after 3sec
        self.assertFalse(os.path.isfile("./thesis.jpg"))

    def test_show_cam_exception(self):
        cam = take_picture.initialize_camera(5)
        isOk = False
        try:
            take_picture.show_cam(cam,30)
        except cv2.error:
            isOk = True

        self.assertTrue(isOk)


class Thread_Keep_Picture(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        blank_image = numpy.zeros(shape=[512, 512, 3], dtype=numpy.uint8)
        take_picture.keep_picture(blank_image,30)

class Thread_Show_Cam(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        cam = take_picture.initialize_camera(0)
        take_picture.show_cam(cam,30)

class Thread_Key_Press(threading.Thread):
    def __init__(self,key,delay):
        threading.Thread.__init__(self)
        self.key = key
        self.delay = delay
    def run(self):
        delayedKeypress(self.key,self.delay)

def removeFile():
    if os.path.isfile("./thesis.jpg"):
        os.remove("./thesis.jpg")

def delayedKeypress(key,delay):      #key gets pressed after funktion starts
    #keyboard = Controller()
    time.sleep(delay)
    keyboard.press(key)

def waitForWindow(name):    #waits for window to open, so key can be pressed
    while cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) < 1:
        #print(cv2.getWindowProperty('Thesis Scanner', cv2.WND_PROP_VISIBLE))
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()