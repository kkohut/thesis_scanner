# from tkinter import *
# from tkinter import messagebox, font
# from PIL import Image, ImageTk
# import thesis_scanner.take_picture as take_picture
#
# import thesis_scanner.Bounding_boxes as BoundingBoxes
# import cv2
#
# img = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
#
#
# root = Tk()
# root.title("Thesis Scanner")
# root.configure(bg = "orange")
# root.attributes("-fullscreen", True)
#
# # root.overrideredirect(True)
#
# myFont = font.Font(size =40, weight = "bold")
#
# def startScanning():
#     # insert method to start scanning
#
#     print("started scanning")
#
# # def enterEmailAdress():
# #     # create new window
# #
# #     emailLabel = Label(frameStep3, text="E-Mail")
# #     emailLabel.place(relx=0.1, rely=0.25)
# #
# #     email2Label = Label(frameStep3, text="Confirm E-Mail")
# #     email2Label.place(relx=0.05, rely=0.3)
# #
# #     emailBox = Entry(frameStep3, width=50, bg="orange")
# #     emailBox.place(relx=0.25, rely=0.25)
# #
# #     emailBox2 = Entry(frameStep3, width=50, bg="orange")
# #     emailBox2.place(relx=0.25, rely=0.3)
# #
# #     submitButton = Button(frameStep3, text="Send Mail")  # insert command = ... that sends mail to student
# #     submitButton.place(relx=0.5, rely=0.4)
#
# #
# # # Step1
# # frameStep1 = LabelFrame(root, text="STEP 1")
# # startButton = Button(frameStep1, text="START", bg="orange", width=25, height=5)
# # startButton.place(relx=0.33, rely=0.25)
# # frameStep1.place(relx=0.01, rely=0.02, relwidth=0.31, relheight=0.95)
# #
# # # Step2
# # frameStep2 = LabelFrame(root, text="STEP 2")
# # # img = ImageTk.PhotoImage()
# # imglabel = Label(frameStep2, text="Show the Image of the Thesis")
# # imglabel.pack()
# # frameStep2.place(relx=0.34, rely=0.02, relwidth=0.31, relheight=0.95)
# #
# # # Step3
# # frameStep3 = LabelFrame(root, text="STEP 3")
# # imglabel = Label(frameStep3, text="Enter Email for Confirmation")
# # imglabel.pack()
# # enterEmailAdress()
# # frameStep3.grid_size()
# # frameStep3.place(relx=0.67, rely=0.02, relwidth=0.31, relheight=0
#
#
# def start():
#     startButton = Button(root, text = "START", bg = "white", command = lambda:[ startButton.place_forget()])
#     startButton["font"] = myFont
#     startButton.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.25)
#
# def showBoundingBoxesImage(img):
#
#     ScanCanvas = Canvas(root)
#     ScanCanvas.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.9)
#
#
# start()
#
#
# root.mainloop()


"""
1. Startseite mit Startbutton und Hinweis "Bitte Arbeit einlegen" -> Kamera startet

2. Seite: Arbeit wird angezeigt -> mit Button "Scannen"

#3. Seite: gescannte Seite mit Bounding Boxes

3. Seite: letzte Seite: Ergebnis des OCR wird angezeigt und vom Studenten bestätigt,
            oder vom Studenten "abgelehnt" mit Neustart
            wenn 2x Neustart gemacht wurde, kann Student Button drücken mit Fehler melden
            Arbeit wird dann gespeichert mit Vermerk, dass nicht alles passt
4. Seite: Arbeit wird gespeichert -> Ladebalken -> wieder zur ersten Seite
"""
import os
import tkinter as tk
import time

from PIL import ImageTk, Image
# from PIL.Image import Image

# import thesis_scanner.take_picture
from PIL.ImageTk import PhotoImage
import cv2

# import thesis_scanner.Bounding_boxes

LARGE_FONT = ("Verdana", 22)


# "main method". Creates the Main Window and displays the corresponding page/frame
class thesisScannerGUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.title(self, "Thesis Scanner")
        # tk.Tk.iconbitmap(self, default = "")

        container = tk.Frame(self)  # container = main window
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)  # 0 is minimum
        container.grid_columnconfigure(0, weight=1)
        self.attributes("-fullscreen", False)  # true if it should be in full screen mode
        # container.configure(bg = "orange")

        self.frames = {}  # dictionary

        for F in (StartPage, PageTwo, PageThree,PageFour):
            frame = F(container, self)

            self.frames[F] = frame

            frame.configure(bg="orange")
            frame.place(anchor="center", relx=0.5, rely=0.5, relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # raise the corresponding page to the top


# define all pages
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="1. Insert your thesis in the scanner\n\n"
                                    "Please make sure the cover page is facing up\n\n"
                                    "2. press \"START\"",
                         font=LARGE_FONT, bg="orange")
        label.place(anchor="center", relx=0.5, rely=0.2)

        startButton = tk.Button(self, text="START", font=LARGE_FONT, bg="white",
                                command=lambda: controller.show_frame(PageTwo))
        startButton.place(anchor="center", relwidth=0.2, relheight=0.2, relx=0.5, rely=0.5)


class PageTwo(tk.Frame):  # show camera and scan the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Press the Scan Button to scan your thesis",
                         font=LARGE_FONT, bg="orange")
        label.place(anchor="center", relx=0.5, rely=0.05)

        scanButton = tk.Button(self, text="SCAN", font=LARGE_FONT, bg="white",
                               command=lambda: controller.show_frame(PageThree))  # change to start scan command
        scanButton.place(anchor="center", relwidth=0.15, relheight=0.08, relx=0.5, rely=0.95)

        cameraCanvas = tk.Canvas(self, bg="white")
        cameraCanvas.place(anchor="center", relwidth=0.35, relheight=0.8, relx=0.5, rely=0.5)

    # thesis_scanner.take_picture.process()

    # photo = PhotoImage(file = r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
    # labelphoto = tk.Label(self, image = photo, )
    # labelphoto.photo = photo
    # labelphoto.place(anchor="center", relwidth = 0.3, relheight = 0.5, relx=0.5, rely=0.5)


class PageThree(tk.Frame):
    # PhotoImage for images in PGM, PPM, GIF and PNG formats.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        name = "Max Musterman" #methods -> Kevin
        thesis = "Entwicklung balblablaba"
        namelabel = tk.Label(self, text="Analyzed Name: {} \n\n"
                                        "Analyzed Thesis: {} ".format(name, thesis),
                             bg="orange", font=LARGE_FONT)
        namelabel.place(anchor="center", relx=0.5, rely=0.5)

        againButton = tk.Button(self, text="Back & Try again", bg="white", font=LARGE_FONT,
                                command=lambda: controller.show_frame(PageTwo))
        againButton.place(anchor="center", relx=0.333, rely=0.8)

        acceptButton = tk.Button(self, text="Accept & Save", bg="white", font=LARGE_FONT,
                                 command = lambda: controller.show_frame(PageFour))
        acceptButton.place(anchor="center", relx=0.666, rely=0.8)

        # scan = Image.open(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
        # scan = scan.resize((x,y), Image.ANTIALIAS)
        # scan = ImageTk.PhotoImage(scan)
        #
        # boundingBoxLabel = tk.Label(self, image = scan)
        # boundingBoxLabel.image = scan
        # boundingBoxLabel.place(anchor = "center", relx = 0.5, rely = 0.5)


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        textLabel = tk.Label(self, text = "Saved in Database", bg="orange", font=LARGE_FONT)
        textLabel.place(anchor="center", relx=0.5, rely=0.5)

        self.after(2000, print("o"))



app = thesisScannerGUI()
app.geometry("1280x720")
app.mainloop()
