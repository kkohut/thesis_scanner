import cv2
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse

import thesis_scanner.take_picture
import thesis_scanner.thesis_scanner_run
import picture_quality_improve
import alignImage
import Rotate_jpg_180
import text_analysis
import os

# RGB, Opacity
Window.clearcolor = (1, .58, 0, 1)
#Window.fullscreen = ("auto")


class Page1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        welcomeLabel = Label(text="1. Insert your thesis in the scanner\n\n"
                                  "Please make sure the cover page is facing up\n\n"
                                  "2. press \"START\"", font_size=30, halign="center",

                             pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.add_widget(welcomeLabel)

        #self.gif = Image(source = r"C:\Users\alexb\Downloads\giphy.gif", anim_delay=0.05)
        #self.add_widget(self.gif)


        self.startButton = Button(text="START", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .5, 'y': .1})

        self.startButton.bind(on_press=self.pushButtonStart)
        self.add_widget(self.startButton)

    def pushButtonStart(self, instance):
        thesis_scanner.take_picture.process()
        thesis_scanner_app.page2.showScan()
        thesis_scanner_app.screenManager.current = "second"



class Page2(FloatLayout):
    img = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.add_widget(Label(text="Page2",pos_hint = {"center_x": 0.5, "center_y":0.7}))

        self.TryAgainButton = Button(text="Try Again", size_hint=(.15, .15), pos_hint={'center_x': .25, 'y': .1})
        self.TryAgainButton.bind(on_press=self.pushButtonTryAgain)
        self.add_widget(self.TryAgainButton)

        self.nextStepButton = Button(text="Next Step", size_hint=(.15, .15), pos_hint={'center_x': .75, 'y': .1})
        self.nextStepButton.bind(on_press=self.pushButtonNextStep)
        self.add_widget(self.nextStepButton)

    def showScan(self):
        source = "thesis0.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'y': .1})
        self.img.reload() #reloads the new image from disk if user trys it again
        self.add_widget(self.img)


    def pushButtonTryAgain(self, _):
        thesis_scanner_app.screenManager.current = "start"


    def pushButtonNextStep(self, instance):
        thesis_scanner_app.page3.analyzeThesis(self.img)
        thesis_scanner_app.screenManager.current = "third"




class Page3(FloatLayout):
    analyzedName = None
    analyzedThesis = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.startAgainButton = Button(text="Try Again", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .25, 'y': .1})
        self.startAgainButton.bind(on_press= self.pushButtonTryAgain)
        self.add_widget(self.startAgainButton)

        self.saveButton = Button(text="Save", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .75, 'y': .1})
        self.saveButton.bind(on_press = self.pushSaveButton)
        self.add_widget(self.saveButton)

    def analyzeThesis(self, img):
        #TODO
        # add all parts to run the scanner
        print("Analyze")




        # text = thesis_scanner.thesis_scanner_run.main()
        # self.analyzedName = "Mario"
        # self.analyzedThesis = "TestThesis"
        # outputText = ("Analayzed Name: "+ self.analyzedName+"\n\nAnalyzed Thesis: "+self.analyzedThesis)
        # self.add_widget(Label(text = outputText, font_size = 20, halign = "center"))

    def pushButtonTryAgain(self,_):
        thesis_scanner_app.screenManager.current = "start"

    def pushSaveButton(self, _):
        thesis_scanner_app.screenManager.current = "start"

class ThesisScannerApp(App):
    def build(self):
        self.screenManager = ScreenManager()

        self.page1 = Page1()
        screen = Screen(name="start")
        screen.add_widget(self.page1)
        self.screenManager.add_widget(screen)

        self.page2 = Page2()
        screen = Screen(name="second")
        screen.add_widget(self.page2)
        self.screenManager.add_widget(screen)

        self.page3 = Page3()
        screen = Screen(name="third")
        screen.add_widget(self.page3)
        self.screenManager.add_widget(screen)

        return self.screenManager


if __name__ == "__main__":
    thesis_scanner_app = ThesisScannerApp()
    thesis_scanner_app.run()
