from datetime import time

import threading
from kivy.uix.label import Label

from threading import Thread

import kivy
from kivy.clock import Clock

kivy.require('1.10.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from thesis_scanner import thesis_scanner_run

# set windowsize to maximum or in fullscreen mode
# Window.maximize()
Window.fullscreen = "auto"  # closable by hitting Alt+F4

# set the background color of the window (r, g, b, alpha) -> (alpha can be understood as opacity)
Window.clearcolor = (1, .58, 0, 1)


class LeftSideButton(Button):
    pass


class RightSideButton(Button):
    pass


class ScreenManager(ScreenManager):
    stop = threading.Event()
    pass


# start screen
class FirstScreen(Screen):
    source = "..\data\paper_input.png"


# camera screen / by Daniel Rindin
class SecondScreen(Screen):

    def on_enter(self, *args):
        # go back to the start screen after 30 seconds
        Clock.schedule_once(self.switch_back, 30)

    def switch_back(self, _):
        # only goes back to first screen if the current screen is the camera screen
        if self.manager.current == "second":
            self.manager.current = "first"
            self.manager.transition.direction = "right"

    def take_photo(self):
        print("saving...")
        self.ids.cam.export_to_png("thesis.png")


# image control screen
class ThirdScreen(Screen):
    # path of the image
    source = "thesis.png"

    def on_pre_enter(self, *args):
        source = "thesis.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'y': .1})
        self.img.reload()
        self.add_widget(self.img)


# loading screen
class FourthScreen(Screen):
    source = "../data/loader.gif"

    def on_enter(self, *args):
        t = Thread(target=self.analyze_thesis)
        t.daemon = True
        t.start()

    def analyze_thesis(self):
        app = App.get_running_app()
        app.ANALYZED_NAME, app.ANALYZED_THESIS = thesis_scanner_run.main()
        self.manager.current = "fifth"


# screen for analyzed data
class FifthScreen(Screen):

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.ids.a_name.text = ("Analyzed Name: " + str(app.ANALYZED_NAME) +
                                "\nAnalyzed Thesis: " + str(app.ANALYZED_THESIS))


class ThesisScannerApp(App):
    ANALYZED_NAME = ""
    ANALYZED_THESIS = ""

    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return ScreenManager()


if __name__ == '__main__':
    ThesisScannerApp().run()
