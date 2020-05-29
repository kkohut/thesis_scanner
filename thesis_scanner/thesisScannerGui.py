import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
import thesis_scanner.take_picture
import thesis_scanner.thesis_scanner_run

# RGB, Opacity
Window.clearcolor = (1, .58, 0, 1)


class Page1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        welcomeLabel = Label(text="1. Insert your thesis in the scanner\n\n"
                                  "Please make sure the cover page is facing up\n\n"
                                  "2. press \"START\"", font_size=30, halign="center",
                             pos_hint={"center_x": 0.5, "center_y": 0.7})
        self.add_widget(welcomeLabel)

        self.nextButton = Button(text="START", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .5, 'y': .1})

        self.nextButton.bind(on_press=self.pushButton)
        self.add_widget(self.nextButton)

    def pushButton(self, instance):
        thesis_scanner.take_picture.process()
        thsesis_scanner_app.page2.getSource()
        thsesis_scanner_app.screenManager.current = "second"



class Page2(FloatLayout):
    img = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.add_widget(Label(text="Page2",pos_hint = {"center_x": 0.5, "center_y":0.7}))

        # self.TryAgainButton = Button(text="Try Again", size_hint=(.15, .15), pos_hint={'center_x': .25, 'y': .1})
        # self.TryAgainButton.bind(on_press=self.pushButtonTryAgain)
        # self.add_widget(self.TryAgainButton)

        self.nextStepButton = Button(text="Next Step", size_hint=(.15, .15), pos_hint={'center_x': .75, 'y': .1})
        self.nextStepButton.bind(on_press=self.pushButtonNextStep)
        self.add_widget(self.nextStepButton)

    def getSource(self):
        source = "thesis0.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'y': .1})
        self.add_widget(self.img)

        #imagecounter wird benötigt, um immer das neueste Bild anzuzeigen

    def pushButtonTryAgain(self, _):
        thsesis_scanner_app.screenManager.current = "start"

    def pushButtonNextStep(self, instance):
        thsesis_scanner_app.page3.analyzeThesis(self.img)
        thsesis_scanner_app.screenManager.current = "third"




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
        #add all parts to run the scanner
        print("Analyze")
        text = thesis_scanner.thesis_scanner_run.main()
        self.analyzedName = "Mario"
        self.analyzedThesis = "TestThesis"
        outputText = ("Analayzed Name: "+ self.analyzedName+"\n\nAnalyzed Thesis: "+self.analyzedThesis)
        self.add_widget(Label(text = outputText, font_size = 20, halign = "center"))

    def pushButtonTryAgain(self,_):
        thsesis_scanner_app.screenManager.current = "start"

    def pushSaveButton(self, _):
        thsesis_scanner_app.screenManager.current = "start"

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
    thsesis_scanner_app = ThesisScannerApp()
    thsesis_scanner_app.run()
