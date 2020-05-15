from tkinter import *
from tkinter import messagebox, font
from PIL import Image, ImageTk


import thesis_scanner.Bounding_boxes as BoundingBoxes
import cv2

img = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")


root = Tk()
root.title("Thesis Scanner")
root.configure(bg = "orange")
root.attributes("-fullscreen", True)

# root.overrideredirect(True)

myFont = font.Font(size =40, weight = "bold")

def startScanning():
    # insert method to start scanning

    print("started scanning")

# def enterEmailAdress():
#     # create new window
#
#     emailLabel = Label(frameStep3, text="E-Mail")
#     emailLabel.place(relx=0.1, rely=0.25)
#
#     email2Label = Label(frameStep3, text="Confirm E-Mail")
#     email2Label.place(relx=0.05, rely=0.3)
#
#     emailBox = Entry(frameStep3, width=50, bg="orange")
#     emailBox.place(relx=0.25, rely=0.25)
#
#     emailBox2 = Entry(frameStep3, width=50, bg="orange")
#     emailBox2.place(relx=0.25, rely=0.3)
#
#     submitButton = Button(frameStep3, text="Send Mail")  # insert command = ... that sends mail to student
#     submitButton.place(relx=0.5, rely=0.4)

#
# # Step1
# frameStep1 = LabelFrame(root, text="STEP 1")
# startButton = Button(frameStep1, text="START", bg="orange", width=25, height=5)
# startButton.place(relx=0.33, rely=0.25)
# frameStep1.place(relx=0.01, rely=0.02, relwidth=0.31, relheight=0.95)
#
# # Step2
# frameStep2 = LabelFrame(root, text="STEP 2")
# # img = ImageTk.PhotoImage()
# imglabel = Label(frameStep2, text="Show the Image of the Thesis")
# imglabel.pack()
# frameStep2.place(relx=0.34, rely=0.02, relwidth=0.31, relheight=0.95)
#
# # Step3
# frameStep3 = LabelFrame(root, text="STEP 3")
# imglabel = Label(frameStep3, text="Enter Email for Confirmation")
# imglabel.pack()
# enterEmailAdress()
# frameStep3.grid_size()
# frameStep3.place(relx=0.67, rely=0.02, relwidth=0.31, relheight=0


def start():
    startButton = Button(root, text = "START", bg = "white", command = lambda:[startScanning(),startButton.place_forget()])
    startButton["font"] = myFont
    startButton.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.25)

def showBoundingBoxesImage(img):

    ScanCanvas = Canvas(root)
    ScanCanvas.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.9)


start()


root.mainloop()
