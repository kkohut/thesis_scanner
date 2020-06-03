import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout

import take_picture
import thesis_scanner_run

# RGB, Opacity
Window.clearcolor = (1, .58, 0, 1)
Window.maximize()  # for develop process


# Window.fullscreen = ("auto") #for final use


class Page1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        infoLabel = Label(text="1. Insert your thesis in the scanner\n\n"
                               "Please make sure the cover page is facing up\n\n"
                               "2. press \"START\"", font_size=30, halign="center",
                          pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.add_widget(infoLabel)

        source = "../data/paper_input.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(.4, .4))
        self.add_widget(self.img)

        self.startButton = Button(text="START", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .5, 'y': .1})
        self.startButton.bind(on_press=self.pushButton_Start)
        self.add_widget(self.startButton)

    def pushButton_Start(self, instance):
        take_picture.process()
        thesis_scanner_app.page2.showScan()
        thesis_scanner_app.screenManager.current = "second"


class Page2(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.TryAgainButton = Button(text="Try Again", size_hint=(.15, .15), pos_hint={'center_x': .25, 'y': .1})
        self.TryAgainButton.bind(on_press=self.pushButton_TryAgain)
        self.add_widget(self.TryAgainButton)

        self.nextStepButton = Button(text="Next Step", size_hint=(.15, .15), pos_hint={'center_x': .75, 'y': .1})
        self.nextStepButton.bind(on_press=self.pushButton_NextStep)
        self.add_widget(self.nextStepButton)

    def showScan(self):
        source = "thesis.jpg"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'y': .1})
        self.img.reload()  # reloads the new image from disk if user trys it again
        self.add_widget(self.img)

    def pushButton_TryAgain(self, _):
        thesis_scanner_app.screenManager.current = "start"

    def pushButton_NextStep(self, instance):
        thesis_scanner_app.page3.analyzeThesis(self.img)
        thesis_scanner_app.screenManager.current = "third"


class Page3(FloatLayout):
    analyzedName = None
    analyzedThesis = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.startAgainButton = Button(text="Try Again", font_size=30, size_hint=(.25, .15),
                                       pos_hint={'center_x': .25, 'y': .1})
        self.startAgainButton.bind(on_press=self.pushButton_TryAgain)
        self.add_widget(self.startAgainButton)

        self.saveButton = Button(text="Save", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .75, 'y': .1})
        self.saveButton.bind(on_press=self.pushSave_Button)
        self.add_widget(self.saveButton)

    def analyzeThesis(self, img):

        self.analyzedName, self.analyzedThesis = thesis_scanner_run.main()

        self.showAnalyzedData()

    def showAnalyzedData(self):
        infoLabel = Label(text="Name: {}\n\nThesis: {}".format(self.analyzedName, self.analyzedThesis),
                          font_size=30,
                          halign="center",
                          pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.add_widget(infoLabel)

    def pushButton_TryAgain(self, _):
        thesis_scanner_app.screenManager.current = "start"

    def pushSave_Button(self, _):
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
